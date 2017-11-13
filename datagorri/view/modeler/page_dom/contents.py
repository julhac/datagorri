import tkinter
from datagorri.view.modeler.page_dom.content import Content
from datagorri.view.component import Component
from datagorri.controller.modeler import Modeler as ModelerController


class Contents(Component):
    def __init__(self, master_frame, rows, repetitive=True, on_repetition_change=None, controller_table_id=None, on_link_adder_click=None, parent_controller_table_id=None, parent_is_repetitive=None):
        Component.__init__(self, master_frame)
        self.get_frame().configure(padx=20)
        self.repetitive = repetitive
        self.on_repetition_change = on_repetition_change
        self.controller_table_id = controller_table_id
        self.parent_controller_table_id = parent_controller_table_id
        self.parent_is_repetitive = parent_is_repetitive

        self.child_tables = []
        self.contents = []

        self.on_link_adder_click = on_link_adder_click

        self.show_content(rows, self.repetitive)

    def show_content(self, rows, repetitive):
        for row_index, row in rows.items():
            row_frame = Contents.create_row_frame(self.get_frame(), row['label'])
            row_frame.pack(side=tkinter.TOP, fill=tkinter.X)

            for col_index, col in row['columns'].items():
                col_label = Contents.create_column_label_frame(self.get_frame(), col['label'])
                col_label.pack(side=tkinter.TOP, fill=tkinter.X)

                # frame for the grid
                col_frame = tkinter.Frame(self.get_frame(), padx=20)
                col_frame.pack(side=tkinter.TOP, fill=tkinter.BOTH)
                at_grid_row = 0

                Contents.create_contents_header(col_frame, at_grid_row)
                at_grid_row += 1

                for content in col['contents']:
                    content_view = Content(
                        col_frame,
                        content['type'],
                        content['value'],
                        at_grid_row,
                        col_index=col_index,
                        row_index=row_index,
                        img_index=content['img_index'] if 'img_index' in content else None,
                        link_index=content['link_index'] if 'link_index' in content else None,
                        add_link_adder=True if content['type'] == 'Link' else False,
                        is_repetitive=repetitive,
                        controller_table_id=self.controller_table_id,
                        parent_controller_table_id=self.parent_controller_table_id,
                        parent_is_repetitive=self.parent_is_repetitive
                    )
                    if self.on_link_adder_click is not None:
                        content_view.on_link_adder_click(self.on_link_adder_click)

                    self.contents.append(content_view)
                    at_grid_row += 1 if not content['type'] == 'Link' else 2  # another line for the link adder btn

                if 'child_tables' in col:
                    for child_index, child_table_content in col['child_tables'].items():
                        child_table_container = tkinter.Frame(self.get_frame(), padx=10)
                        child_table_container.pack(side=tkinter.TOP, fill=tkinter.X)

                        # margin left
                        empty_placeholder_left_frame = tkinter.Frame(child_table_container, width=40)
                        empty_placeholder_left_frame.pack(side=tkinter.LEFT)
                        child_table = ModelerController.create_view_child_table_from_html(child_table_container, child_table_content, child_index, col_index, row_index, child_table_content['is_repetitive'], on_repetition_change=self.on_repetition_change, on_link_adder_click=self.on_link_adder_click, hide_repetition_changer=repetitive, parent_is_repetitive=repetitive)
                        if repetitive:
                            child_table.header.hide_style_change()
                        child_table.get_frame().pack(side=tkinter.TOP, fill=tkinter.X)
                        self.child_tables.append(child_table)
                        empty_placeholder_bottom = tkinter.Frame(child_table_container, height=20)
                        empty_placeholder_bottom.pack(side=tkinter.TOP)

                        at_grid_row += 1

                    empty_placeholder_frame = tkinter.Frame(col_frame, height=10)
                    empty_placeholder_frame.grid(row=at_grid_row, column=0)

    def change_repetition_style(self, repetitive):
        if self.repetitive == repetitive:  # style already in use?
            return True

        self.renew_frame()
        self.get_frame().configure(padx=20)
        self.show_content(repetitive)
        self.repetitive = repetitive

    def get_child_tables(self):
        return self.child_tables

    @staticmethod
    def create_row_frame(master_frame, label):
        row_frame = tkinter.Frame(master_frame)

        row_label = tkinter.Label(
            row_frame,
            text=label,
            bg='#444444',
            fg='#FFFFFF',
            font="Helvetica 16"
        )
        row_label.pack(side=tkinter.LEFT)

        return row_frame

    @staticmethod
    def create_summarized_row_frame(master_frame):
        header_text = 'Summarized rows of the row-repetitive table:'

        row_frame = tkinter.Frame(master_frame)

        row_label = tkinter.Label(
            row_frame,
            text=header_text,
            bg='#444444',
            fg='#FFFFFF',
            font="Helvetica 16"
        )
        row_label.pack(side=tkinter.LEFT, fill=tkinter.X)

        return row_frame

    @staticmethod
    def get_table_header(table_headers, column_index, row_index=None, is_repetitive_table=True):
        if is_repetitive_table and len(table_headers) > column_index:
            to_return = table_headers[column_index].strip()
            if to_return.endswith(':'):
                return to_return[:-1]
            return to_return

        if row_index is not None and len(table_headers) > row_index:
            to_return = table_headers[row_index].strip()
            if to_return.endswith(':'):
                return to_return[:-1]
            return to_return

        return ''

    @staticmethod
    def create_column_label_frame(master_frame, label):
        label_frame = tkinter.Frame(master_frame)

        col_label = tkinter.Label(
            label_frame,
            text=label,
            bg='#222222',
            fg='#FFFFFF',
            font="Helvetica 16"
        )
        col_label.pack(side=tkinter.LEFT, fill=tkinter.X, padx=20)

        return label_frame

    @staticmethod
    def create_contents_header(master_frame, at_grid_row):
        table_head_font = "Helvetica 14 bold"
        tkinter.Label(master_frame, text='Type', font=table_head_font).grid(row=at_grid_row, sticky=tkinter.W)
        tkinter.Label(master_frame, text='Value', font=table_head_font).grid(row=at_grid_row, column=1, sticky=tkinter.W)
        tkinter.Label(master_frame, text='Scrape', font=table_head_font).grid(row=at_grid_row, column=2, sticky=tkinter.W)
        tkinter.Label(master_frame, text='Output-Label', font=table_head_font).grid(row=at_grid_row, column=3, sticky=tkinter.W)

        return True
