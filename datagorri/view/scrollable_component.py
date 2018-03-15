import tkinter


class ScrollableComponent:

    def __init__(self, master_frame):
        self.canvas = tkinter.Canvas(
            master_frame,
            bd=0,
            highlightthickness=0,
            bg='#dedede',
        )
        self.vertical_scrollbar = tkinter.Scrollbar(master_frame, orient=tkinter.VERTICAL, command=self.canvas.yview)
        self.canvas_frame = tkinter.Frame(self.canvas, background="#ffffff")
        self.canvas_frame_id = self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.vertical_scrollbar.set)
        self.canvas.configure(height=self.get_frame().winfo_screenheight()*10)

        self.vertical_scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas_frame.bind('<Configure>', self.configure_canvas_frame)
        self.canvas.bind('<Configure>', self.configure_canvas)

        # Bind mousewheel only if the focus is on the frame otherwise release
        self.canvas_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.canvas_frame.bind('<Leave>', self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event):
        """
        This method is called if the mouse focus is inside the canvas frame to enable scrolling
        :param event: event
        :return: -
        """
        self.canvas_frame.bind_all("<MouseWheel>", self.on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        """
        THis method is called to release the mousewheel if the focus is again outside the canvas frame
        :param event: event
        :return: -
        """
        self.canvas_frame.unbind_all("<MouseWheel>")

    def on_mousewheel(self, event):
        """
        Handles the scrolling mechanism
        :param event: scrolling event
        :return: -
        """
        scroll = 1 if event.num == 5 or event.delta < 0 else -1
        self.canvas.yview_scroll(scroll, "units")

    def configure_canvas_frame(self, event):
        """
        Updates the scrollregion of the canvas_frame to meet the new requirements
        TODO: Some widgets are doubled when scrolling, here are probably changes required.
        :param event: scrolling event
        :return: -
        """
        size = (self.canvas_frame.winfo_reqwidth(), self.canvas_frame.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.canvas_frame.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width=self.canvas_frame.winfo_reqwidth())

    def configure_canvas(self, event):
        """
        Adjusts the widgets to have the required width to span the whole screen
        :param event:
        :return: -
        """
        if self.canvas_frame.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.canvas_frame_id, width=self.canvas.winfo_width())

    def get_frame(self):
        """
        Returns the canvas frame
        :return: the canvas_frame
        """
        return self.canvas_frame


