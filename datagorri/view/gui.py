import os
import tkinter
from tkinter import *
from datagorri.view.navigation import Navigation
from datagorri.view.style import common_style as style

path = os.path.dirname(os.path.abspath(__file__))
pathicon = path+"\\favicon.ico"


class Gui:

    def __init__(self, title, full_screen=True):
        self.frame = tkinter.Tk()
        self.frame.title(title)
        self.frame.wm_iconbitmap(bitmap=pathicon) # include icon
        self.frame.configure(background=style['bg'])

        self.frame.wm_state('zoomed') # start as maximized window

        if full_screen:
            self.do_full_screen()

        header = tkinter.Frame(self.frame)
        header.configure(bg=style['header']['bg'])
        header.pack(side=tkinter.TOP, fill=tkinter.X)

        logo = tkinter.Label(
            header,
            text=title,
            fg=style['logo']['color'],
            bg=style['nav']['bg'],
            padx=style['logo']['padx'],
            font=style['logo']['font']
        )
        logo.pack(side=tkinter.RIGHT)

        self._content = tkinter.Frame(self.frame)
        self._content.pack(side=tkinter.TOP, fill=tkinter.X)

        self._nav = Navigation(header)
        self._nav.get_frame().pack(side=tkinter.LEFT)

    def get_nav(self):
        return self._nav

    def view(self):
        self.frame.mainloop()

    def get_master_frame_of_views(self):
        return self._content

    def do_full_screen(self):
        self.frame.geometry("{0}x{1}+0+0".format(
            self.frame.winfo_screenwidth(),
            self.frame.winfo_screenheight())
        )