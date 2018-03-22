import tkinter

class Tooltip:
    """
    This class represents a tooltip. It can be bound to any tkinter widget.
    """
    def __init__(self, widget, text, waittime=500, wraplength=180):
        self.widget = widget
        self.text = text
        self.waittime = waittime
        self.wraplength = wraplength
        # bind mouse events to show/hide tooltip on enter/exit of mouse
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        
        self.id = None
        self.tw = None
        
    def enter(self, event=None):
        """
        Shows the tooltip window and starts a timer
        """
        self.schedule()
        
    def leave(self, event=None):
        """
        Hides the tooltip window and stops the timer
        """
        self.unschedule()
        self.hide_tooltip()
        
    def schedule(self):
        """
        Stops a previously started timer, shows the tooltip and starts the timer for disappearence.
        """
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.show_tooltip)
        
    def unschedule(self):
        """
        Cancels a probably started timer.
        """
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)
    
    def show_tooltip(self, event=None):
        """
        Creates the tooltip and makes it visible
        """
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # Toplevel window
        self.tw = tkinter.Toplevel(self.widget)
        # show only label, remove app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        
        label = tkinter.Label(self.tw, text=self.text, justify='left', background="#f0f0f0", relief='solid', borderwidth=1, wraplength=self.wraplength)
        label.pack(ipadx=1)
        
    def hide_tooltip(self):
        """
        Destroys the tooltip.
        """
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()
    