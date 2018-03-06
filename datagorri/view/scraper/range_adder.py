import tkinter
import time
from datagorri.view.component import Component
from datagorri.view.style.scraper import style


style = style['scraper']


class RangeAdder(Component):
    def __init__(self, master_frame):
        Component.__init__(self, master_frame)
        self.change_bg('#cccccc')
        self.get_frame().configure(padx=14, pady=20)
        self.get_frame().columnconfigure(2, weight=1)

        tkinter.Label(self.get_frame(), text="ADD MULTIPLE URLS BY RANGE:", font="-weight bold", bg='#cccccc').grid(row=0, column=0, columnspan=3, sticky="NW")
        empty_space = tkinter.Frame(self.get_frame(), height=10, bg='#cccccc')
        empty_space.grid(row=1, column=0)

        tkinter.Label(self.get_frame(), text='URL:', bg='#cccccc').grid(row=2, column=0, sticky='NW')
        self._url=tkinter.Entry(
            self.get_frame(),
            font=style['urlentry']['font'],
            width=40,
            selectborderwidth=0,
            bd=0,
            highlightthickness=0
        )
        self._url.grid(row=3, column=0, columnspan=3, sticky="news", ipady=10)
        self._url.insert(0, 'http://example.example/?id={X}')

        empty_space = tkinter.Frame(self.get_frame(), height=14, bg='#cccccc')
        empty_space.grid(row=4, column=0)

        tkinter.Label(self.get_frame(), text='FROM:', bg='#cccccc').grid(row=5, column=0, sticky='NW')
        self._from=tkinter.Entry(
            self.get_frame(),
            font=style['urlentry']['font'],
            width=13,
            selectborderwidth=0,
            bd=0,
            highlightthickness=0
        )
        self._from.grid(row=6, column=0, sticky="news")
        self._from.insert(0, '0')

        tkinter.Label(self.get_frame(), text='TO:', bg='#cccccc').grid(row=5, column=1, sticky='NW', padx=10)
        self._to=tkinter.Entry(
            self.get_frame(),
            font=style['urlentry']['font'],
            width=13,
            selectborderwidth=0,
            bd=0,
            highlightthickness=0
        )
        self._to.grid(row=6, column=1, sticky="news", padx=10)
        self._to.insert(0, '20')

        self._add_btn = tkinter.Label(
            self.get_frame(),
            text='ADD',
            cursor='hand2',
            bg=style['button']['bg'],
            fg=style['button']['color'],
            font=style['button']['font'],
            padx=style['button']['padx'],
            pady=style['button']['pady']
        )
        self._add_btn.grid(row=6, column=2, sticky="NEWS")

    def on_addition(self, func):
        def handle_click(event):
            self.clickSimulate(self._add_btn)
            func(event)
            time.sleep(0.15)
            self.clickSimulateEnd(self._add_btn)
        self._add_btn.bind('<Button-1>', handle_click)

    def get_url(self):
        return self._url.get()

    def get_range(self):
        return {
            'from': self._from.get(),
            'to':   self._to.get()
        }
