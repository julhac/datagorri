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
        
        frame = tkinter.Frame(self.get_frame())
        frame.pack(side=tkinter.TOP, fill = tkinter.BOTH)
        
        Elements.create_contents_header(frame)
        at_grid_row = 1
        for elem_index, element in elements.items():
            for content in element['elements']:
                print(element)
                elem_view = Element(
                    frame,
                    content['index'],
                    content['type'],
                    content['value'],
                    at_grid_row
                )
                self.elements.append(elem_view)
                at_grid_row += 1
    
    def handle_scrape_all(self, select):
        """
        Selects/Deselects all scrape checkboxes
        """
        for element in self.elements:
            element.handle_scrape_all(select)
    
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
        tkinter.Label(master_frame, text='Index', font=list_head_font).grid(row=0, sticky=tkinter.W)
        tkinter.Label(master_frame, text='Type', font=list_head_font).grid(row=0, column=1, sticky=tkinter.W)
        tkinter.Label(master_frame, text='Value', font=list_head_font).grid(row=0, column=2, sticky=tkinter.W)
        tkinter.Label(master_frame, text='Scrape', font=list_head_font).grid(row=0, column=3, sticky=tkinter.E)
        tkinter.Label(master_frame, text='Output-Label', font=list_head_font).grid(row=0, column=4, sticky=tkinter.E)

        return True