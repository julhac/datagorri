import tkinter

class Element:
    """
    This class represents a line of the elements (including, id, type, value, scrape checkbox and output label textfield)
    """
    def __init__(self, master_frame, index, type, value, at_grid_row):
        self.index = index
        self.type = type
        self.value = value
        
        self.scrape = tkinter.BooleanVar()
        self.label = tkinter.StringVar()
        
        master_frame.columnconfigure(2, weight=1)

        list_head_font = "Helvetica 14"
        tkinter.Label(master_frame, text=index, font=list_head_font).grid(row=at_grid_row, sticky=tkinter.W)
        tkinter.Label(master_frame, text=type, font=list_head_font).grid(row=at_grid_row, column=1, sticky=tkinter.W)
        tkinter.Label(master_frame, text=value, font=list_head_font).grid(row=at_grid_row, column=2, sticky=tkinter.W)
        
        self.scrape_checkbutton = tkinter.Checkbutton(master_frame, variable=self.scrape)
        self.scrape_checkbutton.grid(row=at_grid_row, column=3)
        
        self.label_entry = tkinter.Entry(master_frame, textvariable=self.label)
        self.label_entry.grid(row=at_grid_row, column=4, sticky=tkinter.E)
        self.label_entry.bind("<Key>", lambda event: self._auto_select_scrape_checkbox(event))
    
    def handle_scrape_all(self, select):
        if select:
            self.scrape_checkbutton.select()
        else:
            self.scrape_checkbutton.deselect()
    
    def _auto_select_scrape_checkbox(self, event):
        """
        Selects the scrape checkbox.
        """
        self.scrape_checkbutton.select()
    
    def get_label(self):
        return self.label.get()

    def is_to_scrape(self):
        return self.scrape.get()