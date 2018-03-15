import tkinter
from datagorri.view.modeler.page_dom.list.header import Header
from datagorri.view.modeler.page_dom.list.elements import Elements
from datagorri.view.component import Component

class List(Component):
    """
    This class represents a list. It builds a clickable row for a list. 
    """
    def __init__(self, master_frame, list, list_index):
        Component.__init__(self, master_frame)
        self.change_bg('#222222')
        
        self.list = list
        self.list_index = list_index
        self.expanded = False
        
        self.header = Header(self.get_frame(), list['label'])
        self.header.get_frame().pack(side=tkinter.TOP, fill=tkinter.X)
        self.header.change_cursor(Component.CURSOR_CLICKABLE)
        self.header.change_bg_on_hover('#444444')
        self.header.on_click(lambda e: self.handle_header_click())
        self.header.add_scrape_all_handler(lambda select: self.handle_scrape_all(select))
        
        self.elements = Elements(self.get_frame(), list['elements'])
        
    def get_page_model(self):
        """
        Gathers all information selected to create the page model
        :returns: (Hash) all selected information
        """
        to_scrape = []
        
        for element in self.elements.elements:
            if element.is_to_scrape():
                scrape = {
                    'type': element.type,
                    'elem_index': element.index,
                    'label': element.get_label()
                }
                
                if element.type == 'ImgAlt' or element.type == 'ImgSrc':
                    scrape['img_index'] = element.img_index

                if element.type == 'Link' or element.type == 'LinkText':
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
            'toScrape': to_scrape
        }
        
        if len(nested_lists) > 0:
            result['nestedLists'] = nested_lists
        
        return result
                
    def handle_scrape_all(self, select):
        """
        Selects/Deselects all scrape checkboxes
        """
        self.elements.handle_scrape_all(select)
        
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
        