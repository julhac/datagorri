import json
import requests
import time
from bs4 import BeautifulSoup
from datagorri.model.table import Table
from config.app import config


class Page:
    def __init__(self, html):
        self.html = html
        self.html_as_bs4 = BeautifulSoup(self.get_html(), 'html.parser')

    def get_html_as_bs4(self):
        return self.html_as_bs4

    def get_html(self):
        return self.html

    def get_title(self):
        return self.get_html_as_bs4().title.text

    def get_tables(self):
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

    @staticmethod
    def create_by_url(url, headers=config['request_headers']):
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
        content = dict(
            title=page.get_title(),
            html=page.get_html(),
            url=url,
            timestamp=time.time()
        )
        j = json.dumps(str(content), indent=4)
        f = open(cache_file, 'w+')
        f.write(j)
        f.close()
