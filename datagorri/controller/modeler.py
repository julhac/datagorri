import copy
import datetime
import time
from datagorri.controller import Controller
from urllib.parse import urlparse
from config.app import config
from datagorri.controller.content_types.img import Img
from datagorri.controller.content_types.link import Link
from datagorri.controller.content_types.text import Text
from datagorri.model.page import Page
from datagorri.util.json import Json
from datagorri.model.table.childtable import Childtable
from datagorri.controller.linklist import Linklist


class Modeler(Controller):
    content_types = [Text, Img, Link]
    dropdown_to_update=None
    amount_summarized_examples = 3

    def __init__(self):
        Controller.__init__(self)
        self.url = None
        self.page_dom_tables_unsummarized = []

    def on_route(self, view_class, master_frame):
        if self.view is None:
            self.view = view_class(master_frame, config['default_url'], self.repetition_change, self.scrape_links_for_linklist)

        self.view.on_load_page_dom(self.load_page_dom)
        self.view.on_page_model_create(self.create_model)
        self.view.show()

        return self

    def load_page_dom(self):
        self.url = self.view.get_url_to_load()
        self.page_dom_tables_unsummarized = []

        # load page
        page = Page.create_by_url(self.url)

        if page is False:
            self.view.show_load_page_error()
            return False

        page_dom = dict()
        tables = page.get_tables()
        for table in tables:
            page_dom[table.get_index()] = self._create_table_for_page_dom(table)

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

        self.view.show_page_dom(page_dom)
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

    def _create_table_for_page_dom(self, table, parent_controller_id=None):
        result = dict()
        result['label'] = '#' + str(table.get_index())
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
            cols = self._create_columns_for_page_dom(row, table, parent_controller_id=len(self.page_dom_tables_unsummarized))

            result['rows'][row.get_index()] = {
                'label': 'Row #' + str(row.get_index()) + ':',
                'columns': cols
            }

        result['controller_id'] = len(self.page_dom_tables_unsummarized)  # do not set earlier! Otherwise child_tables controller_id wrong!
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
                child_table = Childtable.create_from_html(child_table_html, child_index, table.get_index(), col.get_index(), row.get_index())

                if table.is_repetitive():
                    child_table.set_repetitive(False)

                child_tables[child_index] = self._create_table_for_page_dom(child_table, parent_controller_id + len(col.get_html_tables()))

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
                if cont['type'] == content['type'] and (not cont['type'] == 'LinkText' or (cont['link_index'] == content['link_index'])):
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
        pm = self.view.get_page_model()
        if pm is False:
            return self

        filename = self.view.get_page_model_name() + '.json'

        timestamp = time.time()
        date = datetime.datetime.fromtimestamp(
            timestamp
        ).strftime('%Y-%m-%d %H:%M:%S')

        result = {
            'tables': pm,
            'url': self.url,
            "timestamp": timestamp,
            "datetime": date
        }

        Json.create_file(config['page_models_dir'] + filename, result)
        self.view.show_pm_success(filename)
        if Modeler.dropdown_to_update is not None:
            Modeler.dropdown_to_update.refresh()

        return self

    def scrape_links_for_linklist(self, controller_table_id, is_repetitive, col_index, link_index, row_index=None, parent_controller_table_id=None, parent_is_repetitive=None):
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
    def create_view_child_table_from_html(master_frame, table, child_index, col_index, row_index, is_repetitive=False, on_repetition_change=None, on_link_adder_click=None, hide_repetition_changer=False, parent_controller_table_id=None, parent_is_repetitive=None):
        child_table = ChildTable(master_frame, table, child_index, col_index, parent_row_index=row_index, on_repetition_change=on_repetition_change, on_link_adder_click=on_link_adder_click, hide_repetition_changer=hide_repetition_changer, parent_is_repetitive=parent_is_repetitive)
        child_table.header.set_repetitive(is_repetitive)
        child_table.change_header_text('Child table #' + str(child_index) + (' of column ' + str(col_index)) if col_index is not None else '')
        return child_table

from datagorri.view.modeler.page_dom.child_table import ChildTable
