from datagorri.view.modeler.page_dom.list.list import List

class NestedList(List):
    """
    This class represents nested lists. It builds a list view within the Elements view.
    """
    def __init__(self, master_frame, list, child_index, parent_element_index, on_repetition_change=None, parent_is_repetitive=None):
        List.__init__(self, master_frame, list, child_index, on_repetition_change=on_repetition_change)
        self.index = child_index
        self.parent_element_index = parent_element_index

        for element in self.elements.elements:
            element.parent_is_repetitive = parent_is_repetitive
        
        self.header.label.configure(pady=4, padx=6)
        
    def get_index(self):
        return self.index
        
    def get_parent_element_index(self):
        return self.parent_element_index