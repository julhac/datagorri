from bs4 import BeautifulSoup
from datagorri.model.table.column import Column


class Row:
    def __init__(self):
        self._index = ''
        self.html = ''
        self.columns = []
        self.bs4 = None

    def __str__(self):
        return str(self.get_html())

    def as_bs4(self):
        return self.bs4

    def get_columns(self):
        return self.columns

    def set_columns(self, columns):
        self.columns = columns

    def get_index(self):
        return self._index

    def set_index(self, index):
        self._index = index

    def get_html(self):
        return self.html

    def set_html(self, html):
        self.html = html

    @staticmethod
    def create_from_html(html):
        row = Row()
        row.set_html(html)

        row.bs4 = BeautifulSoup(html, 'html.parser')

        for index, td in enumerate(row.bs4.find_all("td")):
            # there should be no parents that are td elements
            if len(td.find_parents("td")) != 0:
                continue

            col = Column.create_from_html(str(td))
            col.set_index(len(row.get_columns()))
            row.get_columns().append(col)

        return row
