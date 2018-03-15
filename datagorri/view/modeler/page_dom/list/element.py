import tkinter

class Element:
    """
    This class represents a line of the elements (including, id, type, value, scrape checkbox and output label textfield)
    """
    def __init__(self, master_frame, index, type, value, at_grid_row, img_index=None, link_index=None):
        self.index = index
        self.type = type
        self.value = value
        self.img_index = img_index
        self.link_index = link_index
        
        self.scrape = tkinter.BooleanVar()
        self.label = tkinter.StringVar()
        
        master_frame.columnconfigure(1, weight=1)

        list_head_font = "Helvetica 14"
        tkinter.Label(master_frame, text=type, font=list_head_font).grid(row=at_grid_row, sticky=tkinter.W)
        tkinter.Label(master_frame, text=value, font=list_head_font).grid(row=at_grid_row, column=1, sticky=tkinter.W)
        
        self.scrape_checkbutton = tkinter.Checkbutton(master_frame, variable=self.scrape)
        self.scrape_checkbutton.grid(row=at_grid_row, column=2)
        
        self.label_entry = tkinter.Entry(master_frame, textvariable=self.label)
        self.label_entry.grid(row=at_grid_row, column=3, sticky=tkinter.E)
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
        
    def set_label(self, text):
        self.label.set(text)

    def is_to_scrape(self):
        return self.scrape.get()
        
    def select_to_scrape(self):
        self.scrape_checkbutton.select()