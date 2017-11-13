import tkinter


class Component:
    CURSOR_ADD='plus'
    CURSOR_CLICKABLE='hand2'

    def __init__(self, master_frame):
        self.frame = tkinter.Frame(master_frame)
        self.master_frame = master_frame

    def get_frame(self):
        return self.frame

    def renew_frame(self):
        self.get_frame().destroy()
        self.frame = tkinter.Frame(self.master_frame)

    def change_bg(self, bg):
        self.frame.configure(bg=bg)

    def hide_packed(self):
        self.frame.pack_forget()

    def on_click(self, func):
        self.frame.bind('<Button-1>', func)

    def change_cursor(self, cursor_type):
        self.frame.config(cursor=cursor_type)

    def change_bg_on_hover(self, bg_color):
        old_bg_color = self.frame['background']
        self.frame.bind("<Enter>", lambda e: self.on_hover(self.frame, bg_color=bg_color))
        self.frame.bind("<Leave>", lambda e: self.on_hover_leave(self.frame, bg_color=old_bg_color))

    def on_hover(self, frame, bg_color=None):
        if bg_color is not None:
            frame.configure(bg=bg_color)

    def on_hover_leave(self, frame, bg_color=None):
        if bg_color is not None:
            frame.configure(bg=bg_color)

    @staticmethod
    def clickSimulate(widget):
        widget.configure(bg="#000000")
        widget.configure(foreground="#ffffff")
        widget.update()

    @staticmethod
    def clickSimulateEnd(widget):
        widget.configure(bg="#aaaaaa")
        widget.configure(foreground="#000000")
        widget.update()
