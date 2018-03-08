import tkinter
import time
from datagorri.view.modeler.page_dom.table import Table
from datagorri.view.modeler.resultbar import Resultbar
from datagorri.view.modeler.urlbar import Urlbar
from datagorri.view import View
from datagorri.view.scrollable_component import ScrollableComponent


class Modeler(View):
    """
    This class represents the modeler view. It builds the URL bar and contains the page DOM and result bar after parsing the url.
    """
    def __init__(self, master_frame, default_url='', on_repetition_change=None, on_link_adder_click=None):
        View.__init__(self, master_frame)

        self.on_repetition_change = on_repetition_change
        self.on_link_adder_click = on_link_adder_click
        self.url = Urlbar(self.get_frame(), default_url)
        self.url.get_frame().pack(side=tkinter.TOP, fill=tkinter.X)

        self.pm = Resultbar(self.get_frame(), '')
        self.table_components = []

        self.page_dom = None
        self.page_dom_scrollable_container = None

    def show_page_dom(self, page_dom):
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

        for table_index, table in page_dom.items():
            table_view = Table(self.page_dom_scrollable_container.canvas_frame, table, table_index, self.on_repetition_change, on_link_adder_click=self.on_link_adder_click)
            table_view.get_frame().pack(side=tkinter.TOP, fill=tkinter.X)
            self.table_components.append(table_view)

        self.page_dom.pack(fill=tkinter.BOTH, expand=1)

    def get_page_model(self):
        """
        Gathers all information from the subcomponents which are necessary for the page model.
        """
        result = []

        for table in self.table_components:
            table_result = table.get_page_model()

            if 'childTables' in table_result or len(table_result['toScrape']) > 0:
                result.append(table_result)

        if len(result) < 1:
            self.pm.view_error('Nothing to scrape selected!')
            return False

        labels = []

        for table in result:
            for content in table['toScrape']:
                if content['label'].strip() == '':
                    self.pm.view_error('Some output label is empty!')
                    return False

                if content['label'] in labels:
                    self.pm.view_error('Output label "' + content['label'] + '" is used multiple times!')
                    return False

                labels.append(content['label'])

        return result

    def get_url_to_load(self):
        return self.url.get()
        
    def set_url_to_load(self, url):
        self.url.set(url)
        
    def get_model_to_load(self):
        return self.url.get_selected()

    def set_page_model_name(self, name):
        self.pm.set_name(name)
        return self

    def get_page_model_name(self):
        return self.pm.get_name()

    #def select_include_lists(self):
    #    self.url.select_include_lists()
        
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

