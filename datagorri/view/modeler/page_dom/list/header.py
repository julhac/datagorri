import tkinter
from datagorri.view.component import Component

class Header(Component):
    """
    This class represents the clickable header content for lists
    """
    def __init__(self, master_frame, label, on_scrape_all=None):
        Component.__init__(self, master_frame)
        self.get_frame().configure(padx=16)
        
        self.scrape_all = tkinter.BooleanVar()
        self.scrape_all.set(False)
        self.do_on_scrape_all = []
        if on_scrape_all is not None:
            self.add_scrape_all_handler(on_scrape_all)
            
        self.label = tkinter.Label(
            self.get_frame(),
            text=label,
            bg='#222222',
            fg='#ffffff',
            font='Helvetica 16',
            padx=0,
            pady=8
        )
        self.label.grid(row=0, column=0, sticky=tkinter.W)
        
        self.scrape_all_checkbutton = tkinter.Checkbutton(
            self.get_frame(),
            text="Scrape all",
            variable=self.scrape_all,
            bg="#555555",
            command=self._handle_scrape_all,
            padx=5
        )
        self.scrape_all_checkbutton.grid(row=0, column=1, sticky=tkinter.W)
        
        self.get_frame().columnconfigure(0, weight=1)

        self.change_bg('#222222')
    
    def _handle_scrape_all(self):
        self.scrape_all_checkbutton.update()
        for function in self.do_on_scrape_all:
            function(self.scrape_all.get())
        return True
        
    def add_scrape_all_handler(self, function):
        self.do_on_scrape_all.append(function)
        return self
        
    def on_click(self, func):
        Component.on_click(self, func)
        self.label.bind('<Button-1>', func)

    def change_bg_on_hover(self, bg_color):
        Component.change_bg_on_hover(self, bg_color)
        old_bg_color = self.label['background']
        self.label.bind("<Enter>", lambda event, frame=self.frame: self.on_hover(bg_color))
        self.label.bind("<Leave>", lambda event, frame=self.frame: self.on_hover_leave(old_bg_color))

    def on_hover(self, frame, bg_color=None):
        Component.on_hover(self, self.get_frame(), bg_color)
        self.label.configure(bg=bg_color)

    def on_hover_leave(self, frame, bg_color=None):
        Component.on_hover_leave(self, self.get_frame(), bg_color)
        self.label.configure(bg=bg_color)

    def change_bg(self, bg):
        Component.change_bg(self, bg)
        self.label.configure(bg=bg)