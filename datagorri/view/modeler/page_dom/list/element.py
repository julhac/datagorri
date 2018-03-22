import tkinter

class Element:
    """
    This class represents a line of the elements (including, id, type, value, scrape checkbox and output label textfield)
    """
    def __init__(self, master_frame, index, type, value, at_grid_row, img_index=None, link_index=None, is_repetitive=None, controller_list_id=None, parent_controller_list_id=None, parent_is_repetitive=None):
        self.index = index
        self.type = type
        self.value = value
        self.img_index = img_index
        self.link_index = link_index
        self.controller_list_id = controller_list_id
        self.parent_controller_list_id = parent_controller_list_id
        self.parent_is_repetitive = parent_is_repetitive
        
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
    
    def handle_scrape_all(self, select, level, number):
        """
        Selects/deselects the scrape checkbutton and fills the output label
        :param select: (boolean) True if the checkbutton will be selected, False otherwise
        :param level: (integer) number showing the level
        :param number: (integer) the number the output label should show
        """
        if select:
            self.scrape_checkbutton.select()
            if self.get_label() == "":
                level_str = str(level) + "." if level != 0 else ""
                self.set_label(level_str + str(number))
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