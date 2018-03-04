import tkinter
from datagorri.view.component import Component
from datagorri.view.style.analyzer import style


style = style['urlbar']


class Urlbar(Component):
    def __init__(self, master_frame, default_url=''):
        Component.__init__(self, master_frame)
        self.default_input_text = default_url

        self.change_bg(style['bg'])
        self.get_frame().configure(pady=style['pady'], padx=style['padx'])

        self.input = Urlbar.create_input(self.frame, default_url)
        self.input.grid(row=0, column=0, sticky="nswe")
        self.get_frame().columnconfigure(0, weight=1)

        self.button = Urlbar.create_button(self.frame, 'START')
        self.button.grid(row=0, column=1)

        self.error_label = None

    def get(self):
        return self.input.get()

    def on_click(self, func):
        self.button.bind('<Button-1>', lambda event: func())

    def view_page_load_error(self):
        self.error_label = tkinter.Label(
            self.get_frame(),
            text='Could not load page',
            bg='#b24444',
            padx=10
        )
        self.error_label.grid(row=0, column=2, sticky="news")

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
    def create_input(master_frame, text=''):
        entry = tkinter.Entry(
            master_frame,
            textvariable=tkinter.StringVar(),
            bg=style['input']['bg'],
            fg=style['input']['color'],
            bd=style['input']['border_width'],
            selectborderwidth=style['input']['border_width_select'],
            highlightthickness=0
        )

        entry.insert(tkinter.END, text)

        return entry
