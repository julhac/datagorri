from bs4 import BeautifulSoup
from datagorri.model.table.row import Row


class Table:
    def __init__(self):
        self._index = ''
        self.headers = []
        self.html = ''
        self.child_tables = []
        self.rows = []
        self.css_classes = ''
        self.bs4 = None
        self._is_repetitive = True

    def is_repetitive(self):
        return self._is_repetitive

    def set_repetitive(self, is_repetitive=True):
        self._is_repetitive = is_repetitive
        return self

    def as_bs4(self):
        return self.bs4

    def get_rows(self):
        return self.rows

    def set_rows(self, rows):
        self.rows = rows

    def get_css_classes(self):
        return self.css_classes

    def set_css_classes(self, cssClasses):
        self.css_classes = cssClasses

    def get_index(self):
        return self._index

    def set_index(self, index):
        self._index = index
        return self

    def set_headers(self, headers):
        self.headers = headers

    def get_headers(self):
        return self.headers

    def get_html(self):
        return self.html

    def set_html(self, html):
        self.html = html

    def get_child_tables(self):
        return self.child_tables

    def set_child_tables(self, tables):
        self.child_tables = tables

    @staticmethod
    def create_from_html(html):
        table = Table()
        table.set_html(html)

        table.bs4 = BeautifulSoup(html, 'html.parser')

        if table.bs4.has_attr('class'):
            table.set_css_classes(table.bs4['class'])

        # look for table headers
        for index, th in enumerate(table.bs4.find_all("th")):
            # if not top level, skip
            if len(th.find_parents("th")) != 0:
                continue

            append_x_times = int(th['colspan']) if th.has_attr('colspan') else 1

            for _ in range(append_x_times):
                table.get_headers().append(th.getText())

        # look for child tables
        for index, bchildTable in enumerate(table.bs4.find_all("table")):
            if len(bchildTable.find_parents("table")) == 0:
                continue

            childTable = Table.create_from_html(str(bchildTable))
            table.get_child_tables().append(childTable)

        for index, tr in enumerate(table.bs4.find_all("tr")):
            # there should be no parents that are tr elements
            if len(tr.find_parents("tr")) != 0:
                continue

            row = Row.create_from_html(str(tr))
            row.set_index(len(table.get_rows()))
            table.get_rows().append(row)

        return table
