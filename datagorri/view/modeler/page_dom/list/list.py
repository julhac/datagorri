import tkinter
from datagorri.view.modeler.page_dom.list.header import Header
from datagorri.view.modeler.page_dom.list.elements import Elements
from datagorri.view.component import Component

class List(Component):
    """
    This class represents a list. It builds a clickable row for a list. 
    """
    def __init__(self, master_frame, list, list_index, on_repetition_change=None):
        Component.__init__(self, master_frame)
        self.change_bg('#222222')
        
        self.list = list
        self.list_index = list_index
        self.expanded = False
        self.on_repetition_change = on_repetition_change
        
        self.header = Header(self.get_frame(), list['label'], list['isRepetitive'])
        self.header.get_frame().pack(side=tkinter.TOP, fill=tkinter.X)
        self.header.change_cursor(Component.CURSOR_CLICKABLE)
        self.header.change_bg_on_hover('#444444')
        self.header.on_click(lambda e: self.handle_header_click())
        self.header.add_scrape_all_handler(lambda select: self.handle_scrape_all(select))
        if on_repetition_change is not None:
            self.header.add_repetition_change_handler(lambda is_repetitive: on_repetition_change(list['controller_id'], is_repetitive, self.handle_repetition_change))
        
        self.elements = Elements(self.get_frame(), list['elements'], list['isRepetitive'], on_repetition_change)
        
    def get_page_model(self):
        """
        Gathers all information selected to create the page model
        :returns: (Hash) all selected information
        """
        to_scrape = []
        is_repetitive = self.header.is_repetitive()
        
        for element in self.elements.elements:
            if element.is_to_scrape():
                scrape = {
                    'type': element.type,
                    'elem_index': element.index,
                    'label': element.get_label()
                }
                
                if element.type == 'ImgAlt' or element.type == 'ImgSrc' or element.type == 'ImgTitle':
                    scrape['img_index'] = element.img_index

                if element.type == 'Link' or element.type == 'LinkText' or element.type == 'LinkTitle':
                    scrape['link_index'] = element.link_index

                to_scrape.append(scrape)
                
        nested_lists = []
        for nested_list in self.elements.nested_lists:
            nested_list_result = nested_list.get_page_model()
            if 'nestedLists' in nested_list_result or len(nested_list_result['toScrape']) > 0:
                nested_list_result['parentElementIndex'] = nested_list.get_parent_element_index()
                nested_lists.append(nested_list_result)
                
        result = {
            'listIndex': self.list_index,
            'isRepetitive': is_repetitive,
            'toScrape': to_scrape
        }
        
        if len(nested_lists) > 0:
            result['nestedLists'] = nested_lists
        
        return result
    
    handled_lists = 0 # static variable to count select all clicks of lists
    def handle_scrape_all(self, select):
        """
        Selects/Deselects all scrape checkboxes and enumerates the output labels
        :param select: (boolean) True if the seclect checkboxes should be selected, False otherwise
        """
        self.elements.handle_scrape_all(select, List.handled_lists)
        # update counter
        if select:
            List.handled_lists += 1
        
    def handle_repetition_change(self, new_elems):
        """
        """
        was_expanded = False
        if self.expanded:
            was_expanded = True
            self.narrow()
        
        self.elements.get_frame().destroy()
        self.elements = Elements(self.get_frame(), new_elems, self.header.is_repetitive(), self.on_repetition_change)
        
        if was_expanded:
            self.expand()
        
    def handle_header_click(self):
        """
        expands or collapses the Elements part of the table
        """
        if self.expanded:
            self.narrow()
        else:
            self.expand()

    def expand(self):
        """
        shows the Elements part
        """
        if not self.expanded:
            self.elements.get_frame().pack(side=tkinter.TOP, fill=tkinter.X)
            self.elements.get_frame().update()
            self.expanded = True

    def narrow(self):
        """
        Hides the Elements part
        """
        if self.expanded:
            self.elements.hide_packed()
            self.expanded = False
            
    def change_bg_on_hover(self, bg_color):
        """
        Event function changing the background color of the element when the mouse enters the component
        """
        Component.change_bg_on_hover(self, bg_color)

    def on_hover(self, frame, bg_color=None):
        Component.on_hover(self, self.get_frame(), bg_color=bg_color)
        self.header.on_hover(bg_color)
        
    def change_header_text(self, text):
        self.header.label['text'] = text
        