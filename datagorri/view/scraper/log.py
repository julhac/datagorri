import tkinter
from datagorri.view.component import Component
from datagorri.view.style.scraper import style
from tkinter.scrolledtext import ScrolledText


style = style['scraper']


class Log(Component):
    def __init__(self, master_frame):
        Component.__init__(self, master_frame)

        default_text = 'Log console..\n'
        self.log_text = ScrolledText(self.get_frame(), padx=16, pady=10)
        self.log_text.insert(tkinter.INSERT, default_text)
        self.log_text.configure(height=15)
        self.log_text.grid(row=0,column=0,sticky="news")
        self.log_text.configure(state=tkinter.DISABLED)
        self.get_frame().columnconfigure(0,weight=1)

    def log(self, text):
        self.log_text.configure(state=tkinter.NORMAL)
        self.log_text.see(tkinter.END)
        self.log_text.insert(tkinter.END,text+"\n")
        self.log_text.configure(state=tkinter.DISABLED)
        self.log_text.update()

    def flush(self):
        self.log_text.delete(1.0,"end")
