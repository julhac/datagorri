import tkinter
from datagorri.view.component import Component
from datagorri.view.style.analyzer import style
from datagorri.view.page_model_dropdown import PageModelDropDown

style = style['urlbar']

class Urlbar(Component):
    """
    This class represents the URL bar. It contains a textfield for the URL, a checkbox to in-/exclude lists and a button to load the tables from that URL.
    """
    def __init__(self, master_frame, default_url=''):
        Component.__init__(self, master_frame)
        self.default_input_text = default_url
        
        self.url = tkinter.StringVar()
        self.include_lists = tkinter.BooleanVar()

        self.change_bg(style['bg'])
        self.get_frame().configure(pady=style['pady'], padx=style['padx'])

        # textfield to enter the URL
        self.input = Urlbar.create_input(self.frame, self.url, default_url)
        self.input.grid(row=0, column=0, sticky="nswe")
        self.get_frame().columnconfigure(0, weight=1)

        # checkbox to in-/exclude lists
        self.lists_checkbox = tkinter.Checkbutton(self.frame, text="include lists", variable=self.include_lists)
        self.lists_checkbox.grid(row=0, column=1)
        
        # button to start load action
        self.button = Urlbar.create_button(self.frame, 'START')
        self.button.grid(row=0, column=2)

        self.error_label = None
        
        # dropdown to choose existing page model
        self.pm_drop_down = PageModelDropDown(self.frame)
        self.pm_drop_down.get_frame().grid(row=0, column=4, sticky="news")
        
        # button to load selected page model
        self.load_button = Urlbar.create_button(self.frame, 'LOAD')
        self.load_button.grid(row=0, column=5)

    def get(self):
        return self.url.get()
        
    def set(self, text):
        self.url.set(text)
        
    def get_selected(self):
        return self.pm_drop_down.get_selected()

    def is_include_lists(self):
        return self.include_lists.get()
                
    def select_include_lists(self):
        self.lists_checkbox.select()

    def on_click(self, func):
        self.button.bind('<Button-1>', lambda event: func())
        
    def on_load_click(self, func):
        self.load_button.bind('<Button-1>', lambda event: func())

    def view_load_error(self, what='page'):
        self.error_label = tkinter.Label(
            self.get_frame(),
            text='Could not load ' + what,
            bg='#b24444',
            padx=10
        )
        self.error_label.grid(row=0, column=3, sticky="news")

    def hide_status(self):
        if self.error_label is not None:
            self.error_label.grid_forget()

    @staticmethod
    def create_button(master_frame, text=''):
        return tkinter.Label(
            master_frame,
            cursor='hand2',
            text=text,
            bg=style['button']['bg'],
            fg=style['button']['color'],
            font=style['button']['font'],
            padx=style['button']['padx'],
            pady=style['button']['pady']
        )

    @staticmethod
    def create_input(master_frame, variable, text=''):
        entry = tkinter.Entry(
            master_frame,
            textvariable=variable,
            bg=style['input']['bg'],
            fg=style['input']['color'],
            bd=style['input']['border_width'],
            selectborderwidth=style['input']['border_width_select'],
            highlightthickness=0
        )

        variable.set(text)

        return entry
