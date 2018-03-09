import tkinter
from datagorri.view.modeler.page_dom.list.element import Element
from datagorri.view.component import Component
from datagorri.controller.modeler import Modeler as ModelerController

class Elements(Component):
    """
    This class builds all elements of the list as GUI objects
    """
    def __init__(self, master_frame, elements):
        Component.__init__(self, master_frame)
        self.get_frame().configure(padx=20)
        
        self.elements = []
        self.nested_lists = []
        
        for elem_index, element in elements.items():
            elem_frame = Elements.create_elem_frame(self.get_frame(), element['label'])
            elem_frame.pack(side=tkinter.TOP, fill=tkinter.X)
            
            # frame for the grid
            content_frame = tkinter.Frame(self.get_frame(), padx=20)
            content_frame.pack(side=tkinter.TOP, fill=tkinter.BOTH)
            
            Elements.create_contents_header(content_frame)
            at_grid_row = 1
       
            for content in element['elements']:
                elem_view = Element(
                    content_frame,
                    content['index'],
                    content['type'],
                    content['value'],
                    at_grid_row,
                    img_index=content['img_index'] if 'img_index' in content else None,
                    link_index=content['link_index'] if 'link_index' in content else None,
                )
                self.elements.append(elem_view)
                at_grid_row += 1
                
            if 'nested_lists' in element:
                for child_index, nested_list_content in element['nested_lists'].items():
                    nested_list_container = tkinter.Frame(self.get_frame(), padx=10)
                    nested_list_container.pack(side=tkinter.TOP, fill=tkinter.X)
                    
                    # margin left
                    empty_placeholder_left_frame = tkinter.Frame(nested_list_container, width=40)
                    empty_placeholder_left_frame.pack(side=tkinter.LEFT)
                    
                    nested_list = ModelerController.create_view_nested_list_from_html(nested_list_container, nested_list_content, child_index, elem_index)
                    nested_list.get_frame().pack(side=tkinter.TOP, fill=tkinter.X)
                    self.nested_lists.append(nested_list)
                    
                    empty_placeholder_bottom_frame = tkinter.Frame(nested_list_container, height=20)
                    empty_placeholder_bottom_frame.pack(side=tkinter.TOP)
                    
                    at_grid_row += 1
    
    def handle_scrape_all(self, select):
        """
        Selects/Deselects all scrape checkboxes
        """
        for element in self.elements:
            element.handle_scrape_all(select)
            
    def find_nested_list(self, list_index, parent_element_index):
        """
        Finds a nested list within the list of nested lists by index of the list and index of the parent element
        :param list_index: (Integer) index of the searched list
        :param parent_element_index: (Integer) index of the parent list of the searched list
        :returns: the list with index and parent element index or False
        """
        for list in self.nested_lists:
            if list.index == list_index and list.parent_element_index == parent_element_index:
                return list
        return False
        
    def find_element(self, element_index, type):
        """
        Finds an element within the list of elements by index and type of the element
        :param element_index: (Integer) index of the searched element
        :param type: (string) type of the searched element
        :returns: the element with index and type or False
        """
        for element in self.elements:
            if element.index == element_index and element.type == type:
                return element
        return False
    
    @staticmethod
    def create_elem_frame(master_frame, label):
        elem_frame = tkinter.Frame(master_frame)

        elem_label = tkinter.Label(
            elem_frame,
            text=label,
            bg='#444444',
            fg='#FFFFFF',
            font="Helvetica 16"
        )
        elem_label.pack(side=tkinter.LEFT)

        return elem_frame
        
    @staticmethod
    def create_contents_header(master_frame):
        list_head_font = "Helvetica 14 bold"
        tkinter.Label(master_frame, text='Type', font=list_head_font).grid(row=0, sticky=tkinter.W)
        tkinter.Label(master_frame, text='Value', font=list_head_font).grid(row=0, column=1, sticky=tkinter.W)
        tkinter.Label(master_frame, text='Scrape', font=list_head_font).grid(row=0, column=2, sticky=tkinter.W)
        tkinter.Label(master_frame, text='Output-Label', font=list_head_font).grid(row=0, column=3, sticky=tkinter.W)

        return True