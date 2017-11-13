import tkinter
from datagorri.view.component import Component


class View(Component):
    def __init__(self, master_frame):
        Component.__init__(self, master_frame)

    def show(self):
        # hide old content
        for widget in self.master_frame.winfo_children():
            widget.pack_forget()

        # pack new content
        self.get_frame().pack(side=tkinter.TOP, fill=tkinter.BOTH)
        self.master_frame.update()
