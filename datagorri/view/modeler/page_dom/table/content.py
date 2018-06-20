import tkinter


class Content:
    """
    This class represents a line showing the summary of one column (includes type, sample values of first three rows, a
    scrape checkbox and a output label textfield)
    """
    def __init__(self, master_frame, type, examples, at_grid_row, default_label='', col_index=None, row_index=None, img_index=None,
                 link_index=None, add_link_adder=False, is_repetitive=None, table=None, controller_table_id=None, parent_controller_table_id=None, parent_is_repetitive=None):
        self.type = type
        self.examples = examples
        self.row_index = row_index
        self.col_index = col_index
        self.img_index = img_index
        self.link_index = link_index
        self.link_adder_done = False
        self.scrape = tkinter.BooleanVar()
        self.label = tkinter.StringVar()
        self.do_on_link_adder_click = []
        self.controller_table_id = controller_table_id
        self.parent_is_repetitive=parent_is_repetitive

        master_frame.columnconfigure(1, weight=1)

        table_head_font = "Helvetica 14"
        tkinter.Label(master_frame, text=type, font=table_head_font).grid(row=at_grid_row, sticky=tkinter.W)
        tkinter.Label(master_frame, text=examples, font=table_head_font).grid(row=at_grid_row, column=1,
                                                                              sticky=tkinter.W)
        if add_link_adder:
            self.link_adder = tkinter.Label(master_frame, text='>> Add all similar links to the scraper´s linklist <<', fg="#1393d2", cursor='hand2')
            self.link_adder.grid(row=at_grid_row + 1, column=1, sticky=tkinter.W)
            self.link_adder.bind('<Button-1>', lambda event: self._handle_link_adder_click(self.controller_table_id, is_repetitive, col_index, link_index, row_index, parent_controller_table_id))

        self.scrape_checkbutton = tkinter.Checkbutton(master_frame, variable=self.scrape)
        self.scrape_checkbutton.grid(row=at_grid_row, column=2)

        if not default_label == '':
            self.label.set(default_label)
        self.label_entry = tkinter.Entry(master_frame, textvariable=self.label)
        self.label_entry.grid(row=at_grid_row, column=3, sticky=tkinter.E)
        self.label_entry.bind("<Key>", lambda event: self._auto_select_scrape_checkbox(event)) #5 bind typing to select scrape checkbox

    def handle_scrape_all(self, select, level, number):
        """
        selects the scrape checkbutton and sets the output label

        :param select: (boolean) True if the checkbutton was selected, False otherwise
        :param level: (integer) number of previously select tables
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
        
    def on_link_adder_click(self, function):
        self.do_on_link_adder_click.append(function)

        return self

    def _handle_link_adder_click(self, controller_table_id, is_repetitive, col_index, link_index, row_index, parent_controller_table_id):
        if self.link_adder_done:
            return

        for function in self.do_on_link_adder_click:
            function(controller_table_id, is_repetitive, col_index, link_index, row_index, parent_controller_table_id=parent_controller_table_id, parent_is_repetitive=self.parent_is_repetitive)

        self.link_adder['text'] = 'Done!'
        self.link_adder.update()
        self.link_adder.configure(fg="#13d23d")
        self.link_adder_done = True
        self.link_adder.configure(cursor='')

        return self

    def get_label(self):
        return self.label.get()
        
    def set_label(self, text):
        self.label.set(text)

    def is_to_scrape(self):
        return self.scrape.get()
        
    def select_to_scrape(self):
        self.scrape_checkbutton.select()
