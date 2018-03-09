import copy
import datetime
import time
from config.app import config
from datagorri.controller import Controller
from datagorri.controller.content_types.img import Img
from datagorri.controller.content_types.link import Link
from datagorri.controller.content_types.text import Text
from datagorri.controller.linklist import Linklist
from datagorri.model.page import Page
from datagorri.model.list.nestedlist import Nestedlist
from datagorri.model.table.childtable import Childtable
from datagorri.util.json import Json
from urllib.parse import urlparse

class Modeler(Controller):
    """
    The class provides methods defining the Modeler's behavior.
    """
    content_types = [Text, Img, Link]
    dropdown_to_update = None
    amount_summarized_examples = 3

    def __init__(self):
        Controller.__init__(self)
        self.url = None
        self.page_dom_tables_unsummarized = []

    def on_route(self, view_class, master_frame):
        if self.view is None:
            self.view = view_class(master_frame, config['default_url'], self.repetition_change,
                                   self.scrape_links_for_linklist)

        self.view.on_load_page_dom(self.load_page_dom)
        self.view.on_load_page_model(self.load_page_model)
        self.view.on_page_model_create(self.create_model)
        self.view.show()

        return self

    def load_page_model(self):
        """
        Loads the selected page model and fills in all values
        """
        # load page model
        page_model_name = self.view.get_model_to_load()
        if page_model_name == 'select the page model to use':
            self.view.show_load_error('model')
            return False
        page_model = Controller.load_page_model(config['page_models_dir'] + page_model_name + '.json')
        if not page_model:
            self.view.show_load_error('model')
            return False
        
        # set URL from model and list checkbox
        self.view.set_url_to_load(page_model['url'])
        if 'lists' in page_model and len(page_model['lists']) > 0:
            self.view.select_include_lists()
        
        # load page dom
        self.load_page_dom()
        
        # overwrite default page model name
        self.view.set_page_model_name(page_model_name)
        
        # select scrape checkboxes and fill output label textfields
        for table in page_model['tables']:
            table_component = self.view.table_components[table['tableIndex']]
            table_component.header.select_repetitive(table['isRepetitive'])
            for column in table['toScrape']:
                row_index = column['row_index'] if 'row_index' in column else None
                content = table_component.content.find_content(column['type'], column['col_index'], row_index)
                if not content:
                    print('skip ' + str(column['type']) + ' cell column ' + str(column['col_index']) + ' row ' + str(row_index) + ' in table ' + str(table['tableIndex']))
                    continue
                content.set_label(column['label'])
                content.select_to_scrape()
            if 'childTables' in table:
                self.select_and_fill_child_tables(table_component, table['childTables'])
        
        if 'lists' in page_model: # to support models from old versions
            for list in page_model['lists']:
                list_component = self.view.list_components[list['listIndex']]
                for element in list['toScrape']:
                    content = list_component.elements.find_element(element['elem_index'], element['type'])
                    if not content:
                        print('skip ' + str(element['type']) + ' element ' + str(element['elem_index']) + ' in list #' + str(list['listIndex']))
                        continue
                    content.set_label(element['label'])
                    content.select_to_scrape()
                if 'nestedLists' in list:
                    self.select_and_fill_nested_lists(list_component, list['nestedLists'])
        
    def select_and_fill_child_tables(self, table_component, tables):
        """
        selects cell to scrape and fills output label textfield for child tables
        :param table_component: (Table) component of the parent table containing list of child tables
        :param tables: (dict) content of the childTables key of the page model
        """
        for table in tables:
            parent_row_index = table['parentRowIndex'] if 'parentRowIndex' in table else None
            child_table_component = table_component.content.find_child_table(table['tableIndex'], table['parentColIndex'], parent_row_index)
            if not child_table_component:
                print('skip child table ' + str(table['tableIndex']) + ' of cell column ' + str(table['parentColIndex']) + ' row ' + str(parent_row_index))
                continue
            child_table_component.header.select_repetitive(table['isRepetitive'])
            for column in table['toScrape']:
                row_index = column['row_index'] + 1 if 'row_index' in column else None
                content = child_table_component.content.find_content(column['type'], column['col_index'], row_index)
                if not content:
                    print('skip ' + str(column['type']) + ' cell column ' + str(column['col_index']) + ' row ' + str(row_index) + ' in table ' + str(table['tableIndex']))
                    continue
                content.set_label(column['label'])
                content.select_to_scrape()
            if 'childTables' in table:
                self.select_and_fill_child_tables(child_table_component, table['childTables'])
    
    def select_and_fill_nested_lists(self, list_component, lists):
        """
        selects elements to scrape and fills output label textfields for nested lists 
        :param list_component: (List) component of the parent list containing list of nested lists
        :param lists: (dict) content of the nestedLists key of the page model
        """
        for list in lists:
            nested_list_component = list_component.elements.find_nested_list(list['listIndex'], list['parentElementIndex'])
            if not nested_list_component:
                print('skip nested list ' + str(list['listIndex']) + ' of parent element ' + str(list['parentElementIndex']))
                continue
            for element in list['toScrape']:
                content = nested_list_component.elements.find_element(element['elem_index'], element['type'])
                if not content:
                    print('skip ' + str(element['type']) + ' element ' + str(element['elem_index']) + ' of list #' + str(list['listIndex']))
                    continue
                content.set_label(element['label'])
                content.select_to_scrape()
            if 'nestedLists' in list:
                self.select_and_fill_nested_lists(nested_list_component, list['nestedLists'])
                
        
    def load_page_dom(self):
        """
        Loads the page DOM of the URL and shows tables and lists (if they are included)
        """
        self.url = self.view.get_url_to_load()
        self.page_dom_tables_unsummarized = []

        # load page
        page = Page.create_by_url(self.url)

        if page is False:
            self.view.show_load_error()
            return False

        page_dom_tables = dict()
        tables = page.get_tables()
        for table in tables:
            page_dom_tables[table.get_index()] = self._create_table_for_page_dom(table)
        
        page_dom_lists = dict()
        if self.view.is_include_lists(): # only load lists when checkbox marked
            lists = page.get_lists()
            for list in lists:
                page_dom_lists[list.get_index()] = self._create_list_for_page_dom(list)

        config["current_url"] = self.url
        config["base_url"] = 'http://' + urlparse(config["current_url"])[1]
        config["scheme"] = urlparse(config["current_url"])[0]

        # construct default page model name
        start = self.url.find("http://") if self.url.find("http://") != -1 else self.url.find("https://www.") + 1
        domain = self.url[start + 11:self.url.find(" ", start + 11)]
        domain = domain.split('/')
        domain = domain[0]
        timestamp = time.time()
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H_%M_%S')
        default_page_model_name = domain.replace('.', '_') + '_' + str(date)
        self.view.set_page_model_name(default_page_model_name)

        self.view.show_page_dom(page_dom_tables, page_dom_lists)
        self.view.on_page_model_create(self.create_model)
        return self

    def repetition_change(self, controller_table_id, is_repetitive, change_table_rows_to):
        tables = copy.deepcopy(self.page_dom_tables_unsummarized)
        for table in tables:
            if table['controller_id'] == controller_table_id:
                break

        if is_repetitive:
            table['rows'] = self.summarize_rows_for_page_dom(table['rows'])

        change_table_rows_to(table['rows'])

        return True

    def _create_list_for_page_dom(self, list1):
        result = dict()
        result['label'] = str(list1.get_type()) + ' #' + str(list1.get_type_index())
        result['elements'] = dict()
        
        for element in list1.get_elements():
            elements = []
            for type in Modeler.content_types:
                if type.is_applicable_to(element):
                    content = type.get_content(element)
                    if isinstance(content, list):
                        for single_type_return in content:
                            elements.append(single_type_return)
                    else:
                        elements.append(content)
                        
            nested_lists = {}
            for child_index, nested_list_html in enumerate(element.get_html_lists()):
                nested_list = Nestedlist.create_from_html(nested_list_html, child_index, list1.get_index(), element.get_index())
                nested_lists[child_index] = self._create_list_for_page_dom(nested_list)
                       
            result['elements'][element.get_index()] = {
                'label': 'ListElement #' +  str(element.get_index()),
                'elements': elements,
            }
            
            if len(nested_lists) > 0:
                result['elements'][element.get_index()]['nested_lists'] = nested_lists
                                
        return result
        
    def _create_table_for_page_dom(self, table, parent_controller_id=None):
        result = dict()
        result['label'] = 'Table #' + str(table.get_index())
        result['is_repetitive'] = table.is_repetitive()
        result['rows'] = dict()

        # add table headers to label if existing
        if len(table.get_headers()) > 0:
            result['label'] += ':     '
            last_header = ''
            for index, th in enumerate(table.get_headers()):
                single_header = th.strip(' \t\n\r').replace(':', '')
                if not last_header == single_header:
                    result['label'] += single_header + ', '
                    last_header = single_header

            # remove last ", "
            result['label'] = result['label'][:-2]

        for row in table.get_rows():
            cols = self._create_columns_for_page_dom(row, table,
                                                     parent_controller_id=len(self.page_dom_tables_unsummarized))

            result['rows'][row.get_index()] = {
                'label': 'Row #' + str(row.get_index()) + ':',
                'columns': cols
            }

        result['controller_id'] = len(
            self.page_dom_tables_unsummarized)  # do not set earlier! Otherwise child_tables controller_id wrong!
        if parent_controller_id is not None and parent_controller_id > 0:
            result['parent_controller_id'] = parent_controller_id
        self.page_dom_tables_unsummarized.append(copy.deepcopy(result))

        if table.is_repetitive():
            result['rows'] = Modeler.summarize_rows_for_page_dom(result['rows'])
            
        return result

    def _create_columns_for_page_dom(self, row, table, parent_controller_id):
        result = dict()
        for col in row.get_columns():
            contents = []
            for type in Modeler.content_types:
                if type.is_applicable_to(col):
                    content = type.get_content(col)

                    if isinstance(content, list):
                        for single_type_return in content:
                            contents.append(single_type_return)
                    else:
                        contents.append(content)

            child_tables = {}
            for child_index, child_table_html in enumerate(col.get_html_tables()):
                child_table = Childtable.create_from_html(child_table_html, child_index, table.get_index(),
                                                          col.get_index(), row.get_index())

                if table.is_repetitive():
                    child_table.set_repetitive(False)

                child_tables[child_index] = self._create_table_for_page_dom(child_table, parent_controller_id + len(
                    col.get_html_tables()))

            result[col.get_index()] = {
                'label': 'Column #' + str(col.get_index()),
                'contents': contents,
            }

            if len(child_tables) > 0:
                result[col.get_index()]['child_tables'] = child_tables

        return result

    @staticmethod
    def summarize_rows_for_page_dom(rows):
        cols_result = {}
        if len(rows) < 2:
            return rows

        def type_in_contents(contents, content):
            for cont in contents:
                if cont['type'] == content['type'] and \
                        (not cont['type'] == 'LinkText' or (cont['link_index'] == content['link_index'])):
                    return True

            return False

        def add_value_to_content_type(contents, to_type, val):
            for cont in contents:
                if cont['type'] == to_type:
                    cont['value'] += '  |    ' + val

            return True

        for row_index, row in rows.items():
            for col_index, col in row['columns'].items():
                if col_index not in cols_result:
                    cols_result[col_index] = {'label': col['label'], 'contents': []}

                if 'child_tables' in col:
                    cols_result[col_index]['child_tables'] = col['child_tables']

                for content in col['contents']:
                    if not type_in_contents(cols_result[col_index]['contents'], content):
                        cols_result[col_index]['contents'].append(content)
                    else:
                        add_value_to_content_type(cols_result[col_index]['contents'], content['type'], content['value'])

        # shorten summarized value examples
        for key, col_result in cols_result.items():
            for content in col_result['contents']:
                values = content['value'].split('|')
                content['value'] = '|'.join(values[:Modeler.amount_summarized_examples])

        result = {0: {'label': 'Summarized rows', 'columns': cols_result}}
        return result

    def create_model(self):
        """
        This methods creates a Json file containing a page model in the page model directory
        :return: (object) the self object

        """
        pm = self.view.get_page_model()
        if pm is False:
            return self

        filename = self.view.get_page_model_name() + '.json'

        timestamp = time.time()
        date = datetime.datetime.fromtimestamp(
            timestamp
            ).strftime('%Y-%m-%d %H:%M:%S')

        result = {
            'tables': pm['tables'],
            'lists': pm['lists'],
            'url': self.url,
            "timestamp": timestamp,
            "datetime": date
        }

        Json.create_file(config['page_models_dir'] + filename, result)
        self.view.show_pm_success(filename)
        if Modeler.dropdown_to_update is not None:
            Modeler.dropdown_to_update.refresh()

        return self

    def scrape_links_for_linklist(self, controller_table_id, is_repetitive, col_index, link_index, row_index=None,
                                  parent_controller_table_id=None, parent_is_repetitive=None):
        page_dom = copy.deepcopy(self.page_dom_tables_unsummarized)

        def add_links_from_row(row):
            col = row['columns'][col_index]
            for content in col['contents']:
                if content['type'] == 'Link' and content['link_index'] == link_index:
                    if "http" in content['value']:
                        Linklist.add(content['value'])
                    else:
                        Linklist.add(config['base_url'] + content['value'])

        if parent_is_repetitive:
            tables_with_same_parent = []

            for table in page_dom:
                if 'parent_controller_id' in table and table['parent_controller_id'] == parent_controller_table_id:
                    tables_with_same_parent.append(table)

            for table in tables_with_same_parent:
                for row_index, row in table['rows'].items():
                    if col_index not in row['columns']:
                        continue

                    add_links_from_row(row)
        else:
            for table in page_dom:
                if table['controller_id'] == controller_table_id:
                    break

            if is_repetitive:
                for row_index, row in table['rows'].items():
                    if col_index not in row['columns']:
                        continue

                    add_links_from_row(row)
            elif row_index is not None:
                add_links_from_row(table['rows'][row_index])

        return True

    @staticmethod
    def create_view_nested_list_from_html(master_frame, list, child_index, parent_element_index):
        nested_list = NestedList(master_frame, list, child_index, parent_element_index)
        nested_list.change_header_text('Nested list #' + str(child_index) + ' of element ' + str(parent_element_index))
        return nested_list
        
    @staticmethod
    def create_view_child_table_from_html(master_frame, table, child_index, col_index, row_index, is_repetitive=False,
                                          on_repetition_change=None, on_link_adder_click=None,
                                          hide_repetition_changer=False, parent_controller_table_id=None,
                                          parent_is_repetitive=None):
        child_table = ChildTable(master_frame, table, child_index, col_index, parent_row_index=row_index,
                                 on_repetition_change=on_repetition_change, on_link_adder_click=on_link_adder_click,
                                 hide_repetition_changer=hide_repetition_changer,
                                 parent_is_repetitive=parent_is_repetitive)
        child_table.header.set_repetitive(is_repetitive)
        child_table.change_header_text(
            'Child table #' + str(child_index) + (' of column ' + str(col_index)) if col_index is not None else '')
        return child_table

# keep at bottom of file so there is no circular dependency on startup!!
from datagorri.view.modeler.page_dom.list.nested_list import NestedList ## used in create_view_nested_list_from_html (line 318)
from datagorri.view.modeler.page_dom.table.child_table import ChildTable ## used in create_view_child_table_from_html (line 327)
