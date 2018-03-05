import tkinter
from datagorri.view.modeler.page_dom.header  import Header
from datagorri.view.modeler.page_dom.contents import Contents
from datagorri.view.component                 import Component


class Table(Component):
    """
    This class represents a table. It builds a clickable row for a table. The row contains the index,
    the content of header cells (comma separated and a checkbox determining if the table rows are repetitive.
    """
    def __init__(self, master_frame, table, table_index, on_repetition_change=None, on_link_adder_click=None):
        Component.__init__(self, master_frame)
        self.change_bg('#222222')

        self.table = table
        self.table_index = table_index
        self.expanded = False
        self.on_repetition_change = on_repetition_change
        self.on_link_adder_click = on_link_adder_click
        self.controller_table_id=table['controller_id']
        self.parent_controller_id=table['parent_controller_id'] if 'parent_controller_id' in table else None

        self.header = Header(self.get_frame(), table['label'], table['is_repetitive'])
        self.header.get_frame().pack(side=tkinter.TOP, fill=tkinter.X)
        self.header.change_cursor(Component.CURSOR_CLICKABLE)
        self.header.change_bg_on_hover('#444444')
        self.header.on_click(lambda e: self.handle_header_click())
        self.header.add_scrape_all_handler(lambda select: self.handle_scrape_all(select))
        if on_repetition_change is not None:
            self.header.on_repetition_change(lambda is_repetitive: on_repetition_change(table['controller_id'], is_repetitive, self.handle_repetition_change))
        

        self.content = Contents(self.get_frame(), table['rows'], table['is_repetitive'], on_repetition_change, controller_table_id=self.controller_table_id, on_link_adder_click=on_link_adder_click, parent_controller_table_id=self.parent_controller_id)

    def get_page_model(self):
        """
        Gathers all information selected to create the page model
        returns (Hash): all selected information
        """
        to_scrape = []
        is_repetitive = self.header.is_repetitive()

        for content in self.content.contents:
            if content.is_to_scrape():
                scrape = {
                    'type': content.type,
                    'col_index': content.col_index,
                    'label': content.get_label()
                }

                if not is_repetitive:
                    scrape['row_index'] = content.row_index

                if content.type == 'ImgAlt' or content.type == 'ImgSrc':
                    scrape['img_index'] = content.img_index

                if content.type == 'Link' or content.type == 'LinkText':
                    scrape['link_index'] = content.link_index

                to_scrape.append(scrape)

        child_tables = []
        for child_table in self.content.child_tables:
            child_table_result = child_table.get_page_model()
            if 'childTables' in child_table_result > 0 or len(child_table_result['toScrape']) > 0:
                child_table_result['parentColIndex'] = child_table.get_parent_col_index()
                if not is_repetitive:
                    child_table_result['parentRowIndex'] = child_table.get_parent_row_index()

                child_tables.append(child_table_result)

        result = {
            'tableIndex': self.table_index,
            'isRepetitive': is_repetitive,
            'toScrape': to_scrape
        }

        if len(child_tables):
            result['childTables'] = child_tables

        return result

    def handle_scrape_all(self, select):
        """
        selects/deselects all scrape checkboxes
        """
        self.content.handle_scrape_all(select)
        
    def handle_repetition_change(self, new_rows):
        """
        changes the Contents part when the repetitive rows checkbox value is changed
        """
        was_expanded = False
        if self.expanded:
            was_expanded = True
            self.narrow()

        self.content.get_frame().destroy()
        self.content = Contents(self.get_frame(), new_rows, self.is_repetitive(), self.on_repetition_change, controller_table_id=self.controller_table_id, parent_controller_table_id=self.parent_controller_id, on_link_adder_click=self.on_link_adder_click)

        if was_expanded:
            self.expand()

    def handle_header_click(self):
        """
        expands or collapses the Contents part of the table
        """
        if self.expanded:
            self.narrow()
        else:
            self.expand()

    def expand(self):
        """
        shows the Contents part
        """
        if not self.expanded:
            self.content.get_frame().pack(side=tkinter.TOP, fill=tkinter.X)
            self.content.get_frame().update()
            self.expanded = True

    def narrow(self):
        """
        Hides the Contents part
        """
        if self.expanded:
            self.content.hide_packed()
            self.expanded = False

    def is_repetitive(self):
        return self.header.is_repetitive()

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
