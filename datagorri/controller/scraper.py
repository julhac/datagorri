import time
import datetime
from config.app import config
from datagorri.controller import Controller
from datagorri.model.page import Page
from datagorri.util.csv import Csv
from datagorri.controller.content_types.text import Text as TextTag
from datagorri.controller.content_types.img import Img as ImgTag
from datagorri.controller.content_types.link import Link as LinkTag
from datagorri.model.table import Table
from os import listdir
from os.path import isfile, join
from datagorri.controller.linklist import Linklist


class Scraper(Controller):
    """
    The class scraper provides the methods to scrape the content of tables on specified websites using the previously
    generated page models

    """
    do_on_log_update = []
    links_from_modeler = []

    def __init__(self):
        Controller.__init__(self)
        Linklist.on_update(self.add_link_to_linklist)

    def add_link_to_linklist(self, link):
        Scraper.links_from_modeler.append(link)
        if self.view is not None:
            self.view.add_link_to_linklist(link)

    def on_route(self, view_class, master_frame):
        if self.view is None:
            self.view = view_class(master_frame)

        self.view.show()

        return self

    @staticmethod
    def get_page_models(dir=config['page_models_dir']):
        """
        Returns a list of all page_models at the given path
        :param dir: (string) the directory containing the page_models
        :return: (list) a list containing the page models

        """
        return [f for f in listdir(dir) if isfile(join(dir, f)) and ".json" in f]

    @staticmethod
    def get_link_lists(dir=config['link_lists_dir']):
        """
        Returns a list of all link_lists at the given path
        :param dir: (string) the directory containing the list of links
        :return: (list) a list containing the link lists

        """
        return [f for f in listdir(dir) if isfile(join(dir, f)) and ".txt" in f]

    @staticmethod
    def get_default_link_list_text():
        """

        :return: (string=

        """
        default_links = ''
        for link_from_modeler in Scraper.links_from_modeler:
            default_links += link_from_modeler + '\n'

        return default_links

    @staticmethod
    def get_default_result_filename():
        timestamp = time.time()
        date = datetime.datetime.fromtimestamp(
            timestamp
        ).strftime('%Y-%m-%d_%H-%M-%S')
        return 'result_' + date

    @staticmethod
    def get_default_link_list_file_name():
        timestamp = time.time()
        date = datetime.datetime.fromtimestamp(
            timestamp
        ).strftime('%Y-%m-%d_%H-%M-%S')
        return date

    @staticmethod
    def load_page_model(file):
        if file == '':
            Scraper.update_log('Choose a page model first!')
            return
        else:
            Scraper.update_log('Using page model: ' + file)

            Scraper.update_log('Try: Load page model file: ' + file)
        page_model = Controller.load_page_model(config['page_models_dir'] + file)
        if page_model is False:
            Scraper.update_log('Fail: Could not load page model file: ' + file)
            return False

        Scraper.update_log('Success')
        return page_model

    @staticmethod
    def load_page(url, failures, warnings):
        """
        This method tries to load the given page and return it
        :param url: (string) the url of the page
        :param failures: (list) list of failures
        :param warnings: (list) list of warnings
        :return: (Page)

        """
        page = Page.create_by_url(url)
        max_tries = 5

        # retries
        while page is False and max_tries > 0:
            Scraper.update_log('Warning: Failed. Trying again to load page with url: ' + url)
            warnings.append('Page load failed. Trying again to load page with url: ' + url)
            time.sleep(1)
            page = Page.create_by_url(url)
            max_tries -= 1

        if page is False:
            Scraper.update_log('Fail: Could not load page with url: ' + url)
            failures.append('Could not load page with url: ' + url)
            return False

        return page

    @staticmethod
    def scrape(page_model_file, urls, filename, extension, delimiter):
        """
        This method takes a page_model a list of urls and scrapes the content of the specified websites according
        to the model. The content is then saved in a .csv file.

        :param page_model_file: (string) path to the page_model file
        :param urls: (list) list of urls to scrape
        :param filename: (string) the filename of the generated file
        :param extension: (string) the file extension
        :return: (boolean) Returns True

        """
        failures = []  # Something that definitely went wrong
        warnings = []  # Something that could be wrong
        result_tables = []
        result_lists = []

        # if extension == "choose file extension":
        #    Scraper.update_log("Warning: Choose file extension!")
        #    return

        # Force the delimiter to be 1 char long
        if len(delimiter) != 1:
            Scraper.update_log('Failure: The delimiter must be 1 character long!')
            return

        page_model = Scraper.load_page_model(page_model_file + '.json')
        if not page_model:
            return

        for url in urls:
            Scraper.update_log(' ')
            Scraper.update_log('#############################')
            Scraper.update_log('Scraping: ' + url)
            Scraper.update_log('-----------------------------')

            # load page
            needed_time = time.time()
            Scraper.update_log('Try: Load page')
            page = Scraper.load_page(url, failures, warnings)
            if page is False:
                continue
            needed_time = time.time() - needed_time
            Scraper.update_log(
                'Success: Page has title: ' + page.get_title() + ' (needed time: ' + str(needed_time)[:4] + ' sec.)')
            Scraper.update_log(' ')

            # a list of dicts, may have only one dict if only non-repetitive tables scraped
            table_page_result = []
            for pm_table in page_model['tables']:
                Scraper.update_log('Try: Scrape table #' + str(pm_table['tableIndex']))

                tables = page.get_tables()
                if len(tables) - 1 < pm_table['tableIndex']:
                    Scraper.update_log('Fail: Page has no table with index:' + str(pm_table['tableIndex']))
                    failures.append('Page with url ' + url + ' has no table with index: ' + str(pm_table['tableIndex']))
                    continue

                table_result = Scraper.scrape_table(tables[pm_table['tableIndex']], pm_table['isRepetitive'],
                                                    pm_table['toScrape'], url, pm_table['tableIndex'], failures,
                                                    warnings,
                                                    pm_child_tables=pm_table[
                                                        'childTables'] if 'childTables' in pm_table else [])

                table_page_result = Scraper.add_scraped_table_to_page_scraping(table_result, table_page_result, pm_table['isRepetitive'])
            
            result_tables += table_page_result  # Scraping results in a dict

            list_page_result = []
            for pm_list in page_model['lists']:
                Scraper.update_log('Try: Scrape list #' + str(pm_list['listIndex']))
                
                lists = page.get_lists()
                if len(lists) - 1 < pm_list['listIndex']:
                    Scraper.update_log('Fail: Page has no list with index: ' + str(pm_list['listIndex']))
                    failures.append('Page with URL ' + url + ' has no table with index: ' + str(pm_list['listIndex']))
                    continue
                list_result = Scraper.scrape_list(lists[pm_list['listIndex']], pm_list['toScrape'], url, pm_list['listIndex'], failures, warnings)
                list_page_result = Scraper.add_scraped_list_to_page_scraping(list_result, list_page_result)
            
            result_lists += list_page_result  # Scraping results in a dict
        
        if filename == "":
            timestamp = time.time()
            date = datetime.datetime.fromtimestamp(
                timestamp
            ).strftime('%Y-%m-%d %H:%M:%S')
            date = date.replace(':', '_')
            date = date.replace(' ', '_')
            filename = "result_" + str(date)

        Csv.create_file(config['results_dir'] + filename + ".csv", result_tables, result_lists, delimiter)
        # if extension == ".json":
        #    Json.create_file(config['results_dir'] + filename + ".json", result)
        # else:
        #    Csv.create_file(config['results_dir'] + filename + ".csv", result)

        Scraper.update_log(' ')
        Scraper.update_log('#############################')
        Scraper.update_log('Done!')
        Scraper.update_log(' ')
        Scraper.log_report(failures, warnings)

        return True
    
    @staticmethod
    def add_scraped_list_to_page_scraping(list_result, page_result):
        if len(page_result) == 0:  # no lists on this page scraped so far
            return list_result

        new_page_result = []

        for single_page_result in page_result:
            for single_list_result in list_result:
                new_entry = single_page_result.copy()
                new_entry.update(single_list_result)
                new_page_result.append(new_entry)

        page_result = new_page_result

        return page_result
    
    @staticmethod
    def scrape_list(list, to_scrape, url, list_index, failures, warnings):
        """
        This method scrapes a list and returns a list of dicts
        
        :param list: (List) the list to scrape
        :param to_scrape: (dict) elements to scrape according to the model
        :param url: (string) the url to scrape
        :param list_index: the index of the list to scrape
        :param failures: (list) list of current failures
        :param warnings: (list) list of current warnings
        :return: (list) list of dicts to print in the result file
        """
        list_result = []
        
        for pm_to_scrape in to_scrape:
            Scraper.update_log('Try: Scrape: ' + str(pm_to_scrape))
            
            img_index = pm_to_scrape['img_index'] if 'img_index' in pm_to_scrape else None
            link_index = pm_to_scrape['link_index'] if 'link_index' in pm_to_scrape else None
            
            list_result.append({})
            cont = Scraper.get_list_scrape_val(list, url, list_index, pm_to_scrape['elem_index'], pm_to_scrape['type'], failures, warnings, link_index=link_index, img_index=img_index)
            if not cont:
                continue
            list_result[0][pm_to_scrape['label']] = cont
        
        for single_result in list_result:
            single_result['from_url'] = url
        
        return list_result
        
    @staticmethod
    def add_scraped_table_to_page_scraping(table_result, page_result, is_repetitive):
        if len(page_result) == 0:  # no tables on this page scraped so far
            return table_result

        new_page_result = []

        for single_page_result in page_result:
            for single_table_result in table_result:
                new_entry = single_page_result.copy()
                new_entry.update(single_table_result)
                new_page_result.append(new_entry)

        page_result = new_page_result

        return page_result

    # will return a list of dicts
    @staticmethod
    def scrape_table(table, is_repetitive, to_scrape, url, table_index, failures, warnings, pm_child_tables=[]):
        """
        This method scrapes a table and returns a list of dicts

        :param table:
        :param is_repetitive: (boolean)
        :param to_scrape:
        :param url: (string) the url to scrape
        :param table_index:
        :param failures: (list) list of failures
        :param warnings: (list) list of warnings
        :param pm_child_tables: (list)
        :return: will return a list of dicts

        """
        table_result = []

        for pm_to_scrape in to_scrape:
            Scraper.update_log('Try: Scrape: ' + str(pm_to_scrape))

            img_index = pm_to_scrape['img_index'] if 'img_index' in pm_to_scrape else None
            link_index = pm_to_scrape['link_index'] if 'link_index' in pm_to_scrape else None

            if not is_repetitive:
                table_result.append({})
                suc = Scraper.get_table_scrape_val(table, url, table_index, pm_to_scrape['col_index'],
                                             pm_to_scrape['row_index'],
                                             pm_to_scrape['type'], failures, warnings, link_index=link_index,
                                             img_index=img_index)
                if not suc:
                    continue

                table_result[0][pm_to_scrape['label']] = suc
            else:
                for row_index, row in enumerate(table.get_rows()):
                    suc = Scraper.get_table_scrape_val(table, url, table_index, pm_to_scrape['col_index'], row_index,
                                                 pm_to_scrape['type'], failures, warnings, link_index=link_index,
                                                 img_index=img_index)
                    if not suc:
                        continue

                    while len(table_result) - 1 < row_index:
                        table_result.append({})

                    table_result[row_index][pm_to_scrape['label']] = suc

        table_result = list(filter(None, table_result))

        if len(pm_child_tables) > 0:
            for pm_child_table in pm_child_tables:
                if len(table_result) < 2:
                    rows = table.get_rows()

                    if 'parentRowIndex' not in pm_child_table or len(rows) - 1 < pm_child_table['parentRowIndex']:
                        continue

                    row = rows[pm_child_table['parentRowIndex']]
                    scraped_child = Scraper.scrape_child_table(row, pm_child_table, url, failures, warnings)
                    if scraped_child is False:
                        continue
                else:
                    scraped_child = []
                    for row_index, row in enumerate(table.get_rows()):
                        single_scraped_child = Scraper.scrape_child_table(row, pm_child_table, url, failures, warnings)
                        if single_scraped_child is not False:
                            scraped_child += single_scraped_child

                if 1 < len(table_result) == len(scraped_child):  # parent is repetitive, child not
                    for i in range(0, len(table_result)):
                        table_result[i].update(scraped_child[i])

                elif len(table_result) == 0:  # nothing from parent
                    table_result = scraped_child

                elif len(table_result) == 1 and len(scraped_child) == 1:  # parent and child are not repetitive
                    table_result[0].update(scraped_child[0])

                elif len(table_result) == 1 and len(scraped_child) > 1:  # parent is not repetitive, child is
                    for single_scraped_child in scraped_child:
                        single_scraped_child.update(table_result)

                elif len(table_result) > 1 and len(scraped_child) > 1:
                    bigger_table = table_result if len(table_result) >= len(scraped_child) else scraped_child
                    smaller_table = table_result if len(table_result) < len(scraped_child) else scraped_child
                    for single_entry in bigger_table:
                        single_entry.update(smaller_table[0])

                    table_result = bigger_table

        for single_result in table_result:
            single_result['from_url'] = url

        return table_result

    @staticmethod
    def scrape_child_table(row, pm_child_table, url, failures, warnings):
        cols = row.get_columns()

        if len(cols) - 1 < pm_child_table['parentColIndex']:
            return False

        col = cols[pm_child_table['parentColIndex']]
        html_tables = col.get_html_tables()
        if len(html_tables) - 1 < pm_child_table['tableIndex']:
            return False

        html_table = html_tables[pm_child_table['tableIndex']]
        child_table = Table.create_from_html(html_table)

        further_pm_child_tables = pm_child_table['childTables'] if 'childTables' in pm_child_table else []
        return Scraper.scrape_table(child_table, pm_child_table['isRepetitive'], pm_child_table['toScrape'],
                                    url, pm_child_table['tableIndex'], failures, warnings,
                                    further_pm_child_tables)
    
    @staticmethod
    def get_list_scrape_val(list, url, list_index, element_index, type, failures, warnings, link_index=None, img_index=None):
        elements = list.get_elements()
        
        if len(elements) <= element_index:
            Scraper.update_log('Warning: List has not enough elements: ' + str(len(elements)) + ' actually, but model requires ' + str(element_index + 1))
            failures.append('Element scraping failed for list with index ' + str(list_index) + ' and url ' + url + '. List has not enough elements: ' + str(len(elements)) + 'actually, but model requires ' + str(element_index + 1))
            return False
        
        element = elements[element_index]
        
        if type == 'Text':
            return TextTag.get_val(element)
        elif type == 'ImgAlt':
            return ImgTag.get_alt_val(element, img_index)
        elif type == 'ImgSrc':
            return ImgTag.get_src_val(element, img_index)
        elif type == 'LinkText':
            return LinkTag.get_text_val(element, link_index)
        elif type == 'Link':
            return LinkTag.get_href_val(element, link_index)

        return False
    
    @staticmethod
    def get_table_scrape_val(table, url, table_index, col_index, row_index, type, failures, warnings, link_index=None,
                       img_index=None):
        rows = table.get_rows()

        if len(rows) <= row_index:
            Scraper.update_log(
                'Warning: Table has not enough rows: ' + str(len(rows)) + ' actually, but model requires ' + str(
                    row_index + 1))
            failures.append('Row scraping failed for table with index ' + str(
                table_index) + ' and url ' + url + '. Table has not enough rows: ' + str(
                len(rows)) + 'actually, but model requires ' + str(row_index + 1))
            return False

        row = rows[row_index]
        cols = row.get_columns()

        if len(cols) <= col_index:
            Scraper.update_log('Warning: Table has not enough columns in row: ' + str(row_index))
            warnings.append('Column scraping failed for table with index ' + str(
                table_index) + ' and url ' + url + '. Table has not enough columns in row: ' + str(row_index))
            return False

        col = cols[col_index]

        if type == 'Text':
            return TextTag.get_val(col)
        elif type == 'ImgAlt':
            return ImgTag.get_alt_val(col, img_index)
        elif type == 'ImgSrc':
            return ImgTag.get_src_val(col, img_index)
        elif type == 'LinkText':
            return LinkTag.get_text_val(col, link_index)
        elif type == 'Link':
            return LinkTag.get_href_val(col, link_index)

        return False

    @staticmethod
    def log_report(failures, warnings):
        """
        This method writes the content of failures of warnings to the log file.

        :param failures: (list) list of failures
        :param warnings: (list) list of warnings
        :return: Returns always True

        """
        Scraper.update_log('#############################')
        if len(failures) == 0 and len(warnings) == 0:
            Scraper.update_log('Report: No failures, no warnings!')
            return True

        Scraper.update_log('Report:')
        if len(failures) > 0:
            Scraper.update_log(' ')
            Scraper.update_log('#############################')
            Scraper.update_log(str(len(failures)) + ' Failures:')
            Scraper.update_log('-----------------------------')
            for index, fail in enumerate(failures):
                Scraper.update_log('#' + str(index) + ': ' + fail)
            Scraper.update_log('#############################')
        else:
            Scraper.update_log('No failures')

        if len(warnings) > 0:
            Scraper.update_log(' ')
            Scraper.update_log('#############################')
            Scraper.update_log(str(len(warnings)) + ' Warnings:')
            Scraper.update_log('-----------------------------')
            for index, warning in enumerate(warnings):
                Scraper.update_log('#' + str(index) + ': ' + warning)
        else:
            Scraper.update_log('No warnings')

        return True

    @staticmethod
    def on_log_update(func):
        """
        Appends a given function to the do_on_log_update list
        :param func: (function)
        :return: -

        """
        Scraper.do_on_log_update.append(func)

    @staticmethod
    def update_log(text):
        """
        Takes a string and updates the log with it
        :param text: (string) text
        :return: (boolean) True

        """
        for observer_function in Scraper.do_on_log_update:
            observer_function(text)

        return True

    @staticmethod
    def get_links_by_range(base_url, range_from, range_to):
        """
        This method generates and return a list of URLs based on a given base url and a range of id values appended
        to the end of the url
        :param base_url: (string) the url
        :param range_from: (int) lowest url id
        :param range_to: (int) highest url id
        :return: (list) list of the generated urls

        """
        # swap if from > to:
        if int(range_to) < int(range_from):
            range_to, range_from = range_from, range_to

        urls = []

        for i in range(int(range_from), int(range_to) + 1):
            url = base_url.replace(config["range_placeholder"], str(i))
            urls.append(url)

        return urls

    @staticmethod
    def save_linklist(urls, name=""):
        """
        This method saves a list of links in a .txt file at the link_list directory
        :param urls: (list) list of urls
        :param name: (string) the filename
        :return: (string) return the filename of the created file

        """
        path = config['link_lists_dir']
        if name != "":
            filename = name + ".txt"
        else:
            timestamp = time.time()
            date = datetime.datetime.fromtimestamp(
                timestamp
            ).strftime('%Y-%m-%d_%H-%M')
            date = date.replace(':', '_')
            date = date.replace(' ', '_')
            filename = str(date) + ".txt"

        file = open(path + filename, "w")

        for url in urls:
            file.write(url + "\n")

        file.close()

        return filename

    @staticmethod
    def get_linklist(name):
        """
        This method reads from a given filename in the link_list directory and writes the content into a list.
        :param name: (string) the name of the file
        :return: (list) a list containing the urls

        """
        path = config['link_lists_dir']
        try:
            file = open(path + name + '.txt')
        except PermissionError:
            return "permission_error"
        except FileNotFoundError:
            return "filenotfound_error"
        urls = []
        for line in file:
            line = line.replace("\n", "")
            urls.append(line)

        return urls
