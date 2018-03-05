from datagorri.view.modeler.page_dom.table import Table


class ChildTable(Table):
    """
    This class represents child tables. It builds a table view within the Contents page.
    """
    def __init__(self, master_frame, table, child_index, parent_col_index, parent_row_index=None, on_repetition_change=None, on_link_adder_click=None, hide_repetition_changer=False, parent_is_repetitive=None):
        Table.__init__(self, master_frame, table, child_index, on_repetition_change=on_repetition_change, on_link_adder_click=on_link_adder_click)
        for content in self.content.contents:
            content.parent_is_repetitive=parent_is_repetitive
        self.index = child_index
        self.parent_col_index = parent_col_index
        self.header.label.configure(pady=4, padx=6)
        self.parent_row_index = parent_row_index
        if hide_repetition_changer:
            self.header.repetitive_checkbutton.grid_forget()

    def get_index(self):
        return self.index

    def get_parent_col_index(self):
        return self.parent_col_index

    def get_parent_row_index(self):
        return self.parent_row_index
