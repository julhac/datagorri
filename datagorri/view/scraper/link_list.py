import tkinter
import time
from datagorri.view.component import Component
from datagorri.view.style.scraper import style
from tkinter.scrolledtext import ScrolledText
from datagorri.controller.scraper import Scraper as ScraperController


style = style['scraper']


class LinkList(Component):
    def __init__(self, master_frame):
        Component.__init__(self, master_frame)
        self.change_bg('#dedede')

        self.get_frame().columnconfigure(0, weight=1)

        self._links = ScrolledText(
            self.get_frame(),
            bg="#ffffff",
            borderwidth=0,
            selectborderwidth=0,
            highlightthickness=0,
            font='16',
            height=22
        )
        self._links.grid(row=0, column=0, sticky='NEWS')
        self._links.insert(tkinter.INSERT, ScraperController.get_default_link_list_text())

        tkinter.Frame(self.get_frame(), height=10, bg='#dedede').grid(row=1, column=0, sticky="W")
        tkinter.Label(self.get_frame(), text="SAVE LINKLIST", bg='#dedede').grid(row=2, column=0, sticky="W")

        # Savebar
        self._savebar = tkinter.Frame(self.get_frame())
        self._savebar.grid(row=3, column=0, sticky="NWES")
        self._savebar.columnconfigure(0, weight=1)

        self._new_file_name_entry = tkinter.Entry(
            self._savebar,
            bg=style['input']['bg'],
            fg=style['input']['color'],
            selectborderwidth=0,
            bd=0,
            highlightthickness=0
        )
        self._new_file_name_entry.grid(row=0, column=0, sticky="NEWS")

        self._new_file_btn = tkinter.Label(
            self._savebar,
            text='SAVE',
            cursor='hand2',
            bg=style['button']['bg'],
            fg=style['button']['color'],
            font=style['button']['font'],
            padx=style['button']['padx'],
            pady=style['button']['pady']
        )
        self._new_file_btn.grid(row=0, column=1, sticky="NEWS")

    def on_save(self, func):
        """
        Handles the process after the user clicked on save
        :param func: (function)
        :return: (object)
        """
        def handle_click(event):
            self.clickSimulate(self._new_file_btn)
            func(event)
            time.sleep(0.15)
            self.clickSimulateEnd(self._new_file_btn)
        self._new_file_btn.bind('<Button-1>', handle_click)

    def insert(self, urls):
        if isinstance(urls, list):
            for url in urls:
                if not url == "":
                    if len(self.get()) > 0:
                        self._links.insert(tkinter.END, "\n")
                    self._links.insert(tkinter.END, url)
            self._links.insert(tkinter.END, "\n")
        elif isinstance(urls, str):
            if not urls == "":
                if len(self.get()) > 0:
                    self._links.insert(tkinter.END, "\n")
                self._links.insert(tkinter.END, urls)

        return self

    def get(self):
        links = self._links.get(1.0, tkinter.END)
        links = links.replace(' ', '')
        urls = links.splitlines()
        return list(filter(None, urls))  # filter all empty entries

    def flush(self):
        self._links.delete(1.0, "end")
        return self

    def get_new_file_name(self):
        return self._new_file_name_entry.get()

    def set_new_file_name(self, name):
        self._new_file_name_entry.delete(0, tkinter.END)
        self._new_file_name_entry.insert(0, name)
        return self
