import json
import requests
import time
from bs4 import BeautifulSoup
from datagorri.model.table import Table
from datagorri.model.list.list import List
from config.app import config


class Page:
    def __init__(self, html):
        self.html = html
        self.html_as_bs4 = BeautifulSoup(self.get_html(), 'html.parser')

    def get_html_as_bs4(self):
        return self.html_as_bs4

    def get_html(self):
        """
        Returns the html
        :return: (string)
        """
        return self.html

    def get_title(self):
        """
        Returns the title
        :return: (string)

        """
        return self.get_html_as_bs4().title.text

    def get_tables(self):
        """
        Finds all parent tables located on in html of a website and returns them
        :return: (list) list of found tables
        
        """
        tables = []

        soup = self.get_html_as_bs4()
        for index, table in enumerate(soup.find_all("table")):
            # skip if table has parent table
            if len(table.find_parents("table")) != 0:
                continue

            table = Table.create_from_html(str(table))
            table.set_index(len(tables))
            tables.append(table)

        return tables

    def get_lists(self):
        """
        Finds all lists (ordered and unordered) located on the html of a website and returns them
        :return: (list) list of found lists
        """
        lists = []
        
        soup = self.get_html_as_bs4()
        # get all ordered lists (ol)
        for index, olist in enumerate(soup.find_all("ol")):
            # skip if list has parent list
            if len(olist.find_parents("ol")) != 0 or len(olist.find_parents("ul")) != 0:
                continue
            list = List.create_from_html(str(olist))
            list.set_index(len(lists))
            lists.append(list)
            
        # get all unordered lists (ul)
        for index, ulist in enumerate(soup.find_all("ul")):
            # skip if list has parent list
            if len(ulist.find_parents("ol")) != 0 or len(ulist.find_parents("ul")) != 0:
                continue
            list = List.create_from_html(str(ulist))
            list.set_index(len(lists))
            lists.append(list)
            
        return lists
        
    @staticmethod
    def create_by_url(url, headers=config['request_headers']):
        """
        Returns the received html data from a given url
        :param url: (string) the url
        :param headers: the headers for the content request
        :return: (Page) the html content of the website

        """
        #cache_file = 'cache/pages/' + hashlib.md5(url.encode('utf-8')).hexdigest() + '.json'

        #if use_caching and os.path.exists(cache_file):
        #    data = json.load(open(cache_file))
        #    html = data['html']
        #    return Page(html)

        try:
            page = requests.get(url, headers=headers)

        except requests.exceptions.RequestException as e:
            return False

        page = Page(page.content)
       #Page.create_cache_file(page, cache_file, url)

        return page

    @staticmethod
    def create_cache_file(page, cache_file, url):
        """
        This method generates a cache file containing a dictionary with the content in json format
        :param page: (Page) the page
        :param cache_file: (string) the name of the cache file
        :param url: (string) the name of the corresponding url
        :return: -

        """
        content = dict(
            title=page.get_title(),
            html=page.get_html(),
            url=url,
            timestamp=time.time()
        )
        j = json.dumps(str(content), indent=4)
        with open(cache_file, 'w+') as f:
            f.write(j)
