from datagorri.view.modeler.page_dom.list.list import List

class NestedList(List):
    """
    This class represents nested lists. It builds a list view within the Elements view.
    """
    def __init__(self, master_frame, list, child_index, parent_element_index):
        List.__init__(self, master_frame, list, child_index)
        self.index = child_index
        self.parent_element_index = parent_element_index
        
        self.header.label.configure(pady=4, padx=6)
        
    def get_index(self):
        return self.index
        
    def get_parent_element_index(self):
        return self.parent_element_index