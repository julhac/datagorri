import tkinter
from datagorri.view.component import Component
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

#       filetype_options = ['.csv'] # include ".json": filetype_options = ['.csv', '.json'] ### Include if you want to have JSON as an output option
        self._selected_filetype = tkinter.StringVar()
#       self._filetypes = tkinter.OptionMenu(self.get_frame(), self._selected_filetype, *filetype_options) ### Include if you want to have JSON as an output option
#       self._filetypes.configure(bg='#f0f0f0') ### Include if you want to have JSON as an output option
#       self._filetypes.grid(row=0, column=2, sticky="NEWS") ### Include if you want to have JSON as an output option
        self.select_filetype('.csv')

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
        self._scrape_btn.grid(row=0, column=1, sticky="NEWS")

    def on_scrape(self, function):
        def handle_click(event):
            self.clickSimulate(self._scrape_btn)
            function(event)
            self.clickSimulateEnd(self._scrape_btn)
        self._scrape_btn.bind('<Button-1>', handle_click)

    def select_filetype(self, name):
        self._selected_filetype.set(name)
        return self

    def get_filetype(self):
        return self._selected_filetype.get()

    def get_filename(self):
        return self._filename.get()

    def set_filename(self, name):
        self._filename.delete(0, tkinter.END)
        self._filename.insert(0, name)
        return self