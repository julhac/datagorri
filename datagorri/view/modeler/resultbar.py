import tkinter
from datagorri.view.component import Component
from datagorri.view.style.analyzer import style


style = style['urlbar']


class Resultbar(Component):
    """
    This is the result bar. It contains a textfield where the user can enter a file name for the page model, and a button
    to generate the page model.
    """
    def __init__(self, master_frame, default_page_model_name=None):
        Component.__init__(self, master_frame)

        self.change_bg(style['bg'])
        self.get_frame().configure(pady=style['pady'], padx=style['padx'])

        self.label = tkinter.StringVar()
        if not default_page_model_name is None:
            self.label.set(default_page_model_name)

        self.get_frame().columnconfigure(0, weight=1)

        # textfield to enter the filename
        self.label_entry = tkinter.Entry(
            self.get_frame(),
            textvariable=self.label,
            width=60,
            bg=style['input']['bg'],
            fg=style['input']['color'],
            selectbackground=style['input']['bg_select'],
            bd=style['input']['border_width'],
            selectborderwidth=style['input']['border_width_select']
        )
        self.label_entry.grid(row=0, column=0, sticky="news")

        # button to start generation process
        self.button = tkinter.Label(
            self.get_frame(),
            text='GENERATE PAGE MODEL',
            cursor='hand2',
            bg=style['button']['bg'],
            fg=style['button']['color'],
            font=style['button']['font'],
            padx=style['button']['padx'],
            pady=style['button']['pady']
        )
        self.button.grid(row=0, column=1)

    def set_name(self, name):
        self.label_entry.delete(0, tkinter.END)
        self.label_entry.insert(0, name)
        return self

    def get_name(self):
        return self.label.get()

    def on_create(self, function):
        self.button.bind('<Button-1>', lambda e: function())

    def view_success(self, model_name):
        suc = tkinter.Label(
            self.get_frame(),
            text=model_name + ' successfully generated!',
            bg='#56b256',
            padx=10
        )
        suc.grid(row=0, column=2, sticky="news")

    def view_error(self, error):
        suc = tkinter.Label(
            self.get_frame(),
            text='Error: ' + error,
            bg='#b42121',
            padx=10
        )
        suc.grid(row=0, column=2, sticky="news")
