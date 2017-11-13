from bs4 import BeautifulSoup
from datagorri.model.table import Table
from datagorri.model.table.row import Row


class Childtable(Table):
    def __init__(self, index, parent_index, parent_col_index, parent_row_index=None):
        Table.__init__(self)
        self.set_index(index)
        self._parent_index = parent_index
        self._parent_col_index = parent_col_index
        self._parent_row_index = parent_row_index

    def get_parent_index(self):
        return self._parent_index

    def get_parent_col_index(self):
        return self._parent_col_index

    def get_parent_row_index(self):
        return self._parent_row_index

    @staticmethod
    def create_from_html(html, index, parent_index, parent_col_index, parent_row_index=None):
        table = Childtable(index, parent_index, parent_col_index, parent_row_index)
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
