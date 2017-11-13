import tkinter
from datagorri.view import View
from datagorri.view.scraper.scrapebar import Scrapebar
from datagorri.controller.scraper import Scraper as ScraperController
from datagorri.view.scraper.link_list import LinkList
from datagorri.view.scraper.link_list_dropdown import LinkListDropDown
from datagorri.view.scraper.log import Log
from datagorri.view.scraper.page_model_dropdown import PageModelDropDown
from datagorri.view.scraper.range_adder import RangeAdder
from datagorri.view.scrollable_component import ScrollableComponent
from datagorri.view.style.scraper import style


class Scraper(View):
    def __init__(self, master_frame):
        View.__init__(self, master_frame)
        self.change_bg('#cccccc')

        # Importbar
        importbar = tkinter.Frame(self.get_frame(), pady=style['importbar']['pady'], padx=style['importbar']['padx'],
                                  bg=style['importbar']['bg'])
        importbar.pack(side=tkinter.TOP, fill=tkinter.BOTH)

        self.get_frame().configure()
        tkinter.Label(importbar, text='PAGE MODEL: ', bg=style['importbar']['bg']).grid(row=0, column=0)
        self.page_model = PageModelDropDown(importbar)
        self.page_model.get_frame().grid(row=0, column=1)

        empty_space = tkinter.Frame(importbar, width=24, bg=style['importbar']['bg'])
        empty_space.grid(row=0, column=2)

        tkinter.Label(importbar, text='LINK LIST: ', bg=style['importbar']['bg']).grid(row=0, column=3)
        self.link_list_dropdown = LinkListDropDown(importbar)
        self.link_list_dropdown.get_frame().grid(row=0, column=4)
        self.link_list_dropdown.on_select(lambda selection: self._handle_linklist_select(selection))

        scrollable_frame = ScrollableComponent(self.get_frame())
        # Main
        main_frame = tkinter.Frame(scrollable_frame.get_frame(), pady=30, padx=18, bg='#dedede')
        main_frame.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        main_frame.columnconfigure(0, weight=1)

        tkinter.Label(main_frame, text="URLS TO SCRAPE:", font='-weight bold', bg='#dedede').grid(row=0, column=0,
                                                                                                 sticky="NW")
        self.link_list = LinkList(main_frame)
        self.link_list.get_frame().grid(row=1, column=0, sticky="NEWS")
        self.link_list.set_new_file_name(ScraperController.get_default_link_list_file_name())
        self.link_list.on_save(lambda event: self._handle_linklist_save())

        # Sidebar
        sidebar = tkinter.Frame(main_frame, padx=20, bg='#dedede')
        sidebar.grid(row=1, column=1, sticky="NW")

        self.range_adder = RangeAdder(sidebar)
        self.range_adder.get_frame().grid(row=1, column=0, sticky="NEWS")
        self.range_adder.on_addition(lambda event: self._handle_range_addition())

        # scrapebar
        self._scrapebar = Scrapebar(scrollable_frame.get_frame())
        self._scrapebar.get_frame().pack(side=tkinter.TOP, fill=tkinter.X)
        self._scrapebar.set_filename(ScraperController.get_default_result_filename())
        self._scrapebar.on_scrape(lambda event: self._handle_scraping())

        # Log
        logbar = tkinter.Frame(scrollable_frame.get_frame(), pady=0, padx=0, bg='#cccccc')
        logbar.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        logbar.columnconfigure(0, weight=1)

        # tkinter.Label(logbar, text='OUTPUT', bg='#cccccc', pady=12).grid(row=0, column=0, sticky="W")
        self.log = Log(logbar)
        self.log.get_frame().grid(row=1, column=0, sticky="NEWS")
        ScraperController.on_log_update(lambda log_entry: self.log.log(log_entry))

    def add_link_to_linklist(self, link):
        self.link_list.insert(link)
        return self

    def _handle_linklist_select(self, selection):
        self.link_list.flush()
        urls = ScraperController.get_linklist(selection)
        if urls == "permission_error":
            self.log.log('Warning: Permission error')
            return
        elif urls == "filenotfound_error":
            self.log.log('Warning: FileNotFound error')
            return
        self.link_list.insert(urls)
        self.link_list.set_new_file_name(selection)
        self.log.log('Imported linklist ' + selection)

        return self

    def _handle_linklist_save(self):
        filename = self.link_list.get_new_file_name()
        ScraperController.save_linklist(self.link_list.get(), filename)
        self.link_list_dropdown.select(filename)
        self.link_list_dropdown.refresh()
        self.log.log('Saved links to linklist ' + filename)

        return self

    def _handle_range_addition(self):
        self.link_list.insert(
            ScraperController.get_links_by_range(self.range_adder.get_url(), self.range_adder.get_range()['from'],
                                                 self.range_adder.get_range()['to']))
        self.log.log('Added links by range')
        return self

    def _handle_scraping(self):
        self.log.log('Start scraping')
        ScraperController.scrape(self.page_model.get_selected(), self.link_list.get(), self._scrapebar.get_filename(),
                                self._scrapebar.get_filetype())
        return self
