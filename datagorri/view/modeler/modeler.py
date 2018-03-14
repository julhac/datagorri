import tkinter
import time
from datagorri.view.modeler.page_dom.table.table import Table
from datagorri.view.modeler.page_dom.list.list import List
from datagorri.view.modeler.resultbar import Resultbar
from datagorri.view.modeler.urlbar import Urlbar
from datagorri.view import View
from datagorri.view.scrollable_component import ScrollableComponent


class Modeler(View):
    """
    This class represents the modeler view. It builds the URL bar and contains the page DOM and result bar after parsing the url.
    """
    def __init__(self, master_frame, default_url='', on_table_repetition_change=None, on_list_repetition_change=None, on_link_adder_click=None):
        View.__init__(self, master_frame)

        self.on_table_repetition_change = on_table_repetition_change
        self.on_list_repetition_change = on_list_repetition_change
        self.on_link_adder_click = on_link_adder_click
        self.url = Urlbar(self.get_frame(), default_url)
        self.url.get_frame().pack(side=tkinter.TOP, fill=tkinter.X)

        self.pm = Resultbar(self.get_frame(), '')
        self.table_components = []
        self.list_components = []

        self.page_dom = None
        self.page_dom_scrollable_container = None

    def show_page_dom(self, page_dom_tables, page_dom_lists):
        """
        Shows the page DOM as result of parsing the URLs page.
        
        params (): page DOM to show
        """
        self.url.hide_status()
        if self.page_dom is not None:
            self.page_dom_scrollable_container.canvas.destroy()
            self.pm.get_frame().destroy()
            self.pm = Resultbar(self.get_frame(), self.get_page_model_name())
            self.page_dom.destroy()
            self.table_components = []

        self.page_dom = None
        self.pm.get_frame().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH)

        self.page_dom = tkinter.Frame(self.get_frame())
        self.page_dom_scrollable_container = ScrollableComponent(self.page_dom)

        for table_index, table in page_dom_tables.items():
            table_view = Table(self.page_dom_scrollable_container.canvas_frame, table, table_index, self.on_table_repetition_change, on_link_adder_click=self.on_link_adder_click)
            table_view.get_frame().pack(side=tkinter.TOP, fill=tkinter.X)
            self.table_components.append(table_view)
            
        for list_index, list in page_dom_lists.items():
            list_view = List(self.page_dom_scrollable_container.canvas_frame, list, list_index, self.on_list_repetition_change)
            list_view.get_frame().pack(side=tkinter.TOP, fill=tkinter.X)
            self.list_components.append(list_view)

        self.page_dom.pack(fill=tkinter.BOTH, expand=1)

    def get_page_model(self):
        """
        Gathers all information from the subcomponents which are necessary for the page model.
        :returns: (Hash or boolean) the list of elements or False
        """
        result = dict()
        result['tables'] = []
        result['lists'] = []

        # gather all tables
        for table in self.table_components:
            table_result = table.get_page_model()

            if 'childTables' in table_result or len(table_result['toScrape']) > 0:
                result['tables'].append(table_result)

        # gather all lists
        for list in self.list_components:
            list_result = list.get_page_model()
            if 'nestedLists' in list_result or len(list_result['toScrape']) > 0:
                result['lists'].append(list_result)
        
        # check if something was selected to scrape
        if len(result['tables']) + len(result['lists']) < 1:
            self.pm.view_error('Nothing to scrape selected!')
            return False

        labels = dict()
        labels['tables'] = []
        labels['lists'] = []

        # gather all table labels (cancel if empty or duplicate use)
        for table in result['tables']:
            for content in table['toScrape']:
                if content['label'].strip() == '':
                    self.pm.view_error('Some table output label is empty!')
                    return False

                if content['label'] in labels['tables']:
                    self.pm.view_error('Output label "' + content['label'] + '" is used multiple times for tables!')
                    return False

                labels['tables'].append(content['label'])
        
        # gather all list labels (cancel if empty or duplicate use)
        for list in result['lists']:
            for element in list['toScrape']:
                if element['label'].strip() == '':
                    self.pm.view_error('Some list output label is empty!')
                if element['label'] in labels['lists']:
                    self.pm.view_error('Output label "' + content['label'] + '" is used multiple times for lists!')
                    return False
                labels['lists'].append(element['label'])

        return result

    def get_url_to_load(self):
        return self.url.get()
        
    def set_url_to_load(self, url):
        self.url.set(url)
        
    def get_model_to_load(self):
        return self.url.get_selected()

    def is_include_lists(self):
        return self.url.is_include_lists()
        
    def set_page_model_name(self, name):
        self.pm.set_name(name)
        return self

    def get_page_model_name(self):
        return self.pm.get_name()

    def select_include_lists(self):
        self.url.select_include_lists()
        
    def show_load_error(self, what='page'):
        self.url.view_load_error(what)
        return self

    def on_load_page_dom(self, function):
        def handle_click():
            self.clickSimulate(self.url.button)
            function()
            self.clickSimulateEnd(self.url.button)

        self.url.on_click(handle_click)
        return self
        
    def on_load_page_model(self, function):
        def handle_click():
            self.clickSimulate(self.url.load_button)
            function()
            self.clickSimulateEnd(self.url.load_button)
            
        self.url.on_load_click(handle_click)
        return self

    def on_page_model_create(self, function):
        def handle_click():
            self.clickSimulate(self.pm.button)
            function()
            time.sleep(0.15)
            self.clickSimulateEnd(self.pm.button)

        self.pm.on_create(handle_click)
        return self

    def show_pm_success(self, pm_name):
        self.pm.view_success(pm_name)

