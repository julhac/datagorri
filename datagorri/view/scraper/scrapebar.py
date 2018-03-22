import tkinter
from datagorri.view.component import Component
from datagorri.view.tooltip import Tooltip
from datagorri.view.style.scraper import style
style = style['scraper']


class Scrapebar(Component):
    def __init__(self, master_frame):
        Component.__init__(self, master_frame)
        self.get_frame().configure(pady=20, padx=18)
        self.change_bg('#f0f0f0')
        self.get_frame().columnconfigure(0, weight=1)

        self._filename = tkinter.Entry(
            self.get_frame(),
            bg=style['input']['bg'],
            fg=style['input']['color'],
            selectborderwidth=0,
            bd=0,
            highlightthickness=0
        )
        self._filename.grid(row=0, column=0, sticky="NEWS")

#       filetype_options = ['.csv'] # include ".json": filetype_options = ['.csv', '.json'] ### Include if you want to
        # have JSON as an output option
        self._selected_filetype = tkinter.StringVar()
#       self._filetypes = tkinter.OptionMenu(self.get_frame(), self._selected_filetype, *filetype_options) ### Include
        # if you want to have JSON as an output option
#       self._filetypes.configure(bg='#f0f0f0') ### Include if you want to have JSON as an output option
#       self._filetypes.grid(row=0, column=2, sticky="NEWS") ### Include if you want to have JSON as an output option
        self.select_filetype('.csv')

        tkinter.Label(self.get_frame(), text='Delimiter:', bg='#cccccc').grid(row=0, column=1, sticky="NEWS", padx=10)
        self._delimiter = tkinter.Entry(
            self.get_frame(),
            bg=style['input']['bg'],
            fg=style['input']['color'],
            width=5,
            selectborderwidth=0,
            bd=0,
            highlightthickness=0
        )
        self._delimiter.grid(row=0, column=2, sticky="NEWS")
        self._delimiter.insert(0, ';')
        
        tkinter.Label(self.get_frame(), text='Encoding:', bg='#cccccc').grid(row=0, column=3, sticky="NEWS", padx=10)
        self._encoding = tkinter.StringVar(self.get_frame())
        self._encoding_dropdown = tkinter.OptionMenu(self.get_frame(), self._encoding, "UTF-8", "Latin-1")
        self._encoding_dropdown.config(width=10)
        self._encoding_dropdown.grid(row=0, column=4, sticky="NEWS")
        self._encoding.set("UTF-8")
        # Tooltip
        self._encoding_tooltip = Tooltip(self._encoding_dropdown, "Most websites are encoded in UTF-8. So using Latin-1 here might cause problems!")
        
        self._scrape_btn = tkinter.Label(
            self.get_frame(),
            text='SCRAPE',
            cursor='hand2',
            bg=style['button']['bg'],
            fg=style['button']['color'],
            font=style['button']['font'],
            padx=style['button']['padx'],
            pady=style['button']['pady']
        )
        self._scrape_btn.grid(row=0, column=5, sticky="NEWS", padx=(10, 0))

    def on_scrape(self, func):
        """
        Handles the scrape button onclick action
        :param func: (function)
        :return: -
        """
        def handle_click(event):
            self.clickSimulate(self._scrape_btn)
            func(event)
            self.clickSimulateEnd(self._scrape_btn)
        self._scrape_btn.bind('<Button-1>', handle_click)

    def select_filetype(self, name):
        self._selected_filetype.set(name)
        return self

    def get_filetype(self):
        return self._selected_filetype.get()

    def get_filename(self):
        """
        Returns the filename
        :return: (string) the filename
        """
        return self._filename.get()

    def set_filename(self, name):
        """
        Sets the filename
        :param name: (string) the filename
        :return: (object)
        """
        self._filename.delete(0, tkinter.END)
        self._filename.insert(0, name)
        return self

    def get_delimiter(self):
        """
        Returns the delimiter value
        :return: (string) the delimiter
        """
        return self._delimiter.get()
        
    def get_encoding(self):
        """
        Returns the encoding value
        :return: (string) the encoding
        """
        return self._encoding.get()
