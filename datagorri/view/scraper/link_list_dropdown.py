import tkinter
from datagorri.view.component     import Component
from datagorri.view.style.scraper import style
from datagorri.controller.scraper import Scraper as ScraperController


style = style['link_list_dropdown']


class LinkListDropDown(Component):
    def __init__(self, master_frame):
        Component.__init__(self, master_frame)
        self._do_on_select = []

        self._selected = tkinter.StringVar()
        self.no_links_label = None
        self._linklists = dict()
        linklist_files = ScraperController.get_link_lists()
        for linklist_file in linklist_files:
            self._linklists[linklist_file.replace('.txt', '')] = linklist_file.replace('.txt', '')

            len_longest_name = len(max(linklist_files, "                                          ", key=len))
        if len(self._linklists) > 0:
            self._link_list_option_menu = tkinter.OptionMenu(self.get_frame(), self._selected, *self._linklists.keys(), command=lambda e: self._handle_select())
            self._link_list_option_menu.config(width=len_longest_name)
            self._link_list_option_menu.configure(bg=style['bg'])
            self._link_list_option_menu.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
            self.select("select to import a linklist")
        else:
            self.no_links_label = tkinter.Label(self.get_frame(), text="No linklists available!", bg=style['bg'])
            self.no_links_label.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    def select(self, name):
        self._selected.set(name)
        self._handle_select()
        return self

    def on_select(self, function):
        self._do_on_select.append(function)
        return self

    def _handle_select(self):
        for function in self._do_on_select:
            function(self.get_selected())

        return self

    def get_selected(self):
        return self._selected.get()

    def get_all(self):
        link_lists = []
        for linklist in self._linklists:
            if linklist is not None:
                link_lists.append(linklist)

        return link_lists

    def refresh(self):
        linklist_files = ScraperController.get_link_lists()

        if self.no_links_label is not None:
            len_longest_name = len(max(linklist_files, key=len))
            for linklist_file in linklist_files:
                self._linklists[linklist_file.replace('.txt', '')] = linklist_file.replace('.txt', '')

            self.no_links_label.destroy()
            self._link_list_option_menu = tkinter.OptionMenu(self.get_frame(), self._selected, *self._linklists.keys(),
                                                             command=lambda e: self._handle_select())
            self._link_list_option_menu.config(width=len_longest_name)
            self._link_list_option_menu.configure(bg=style['bg'])
            self._link_list_option_menu.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
            self.no_links_label = None
        else:
            for item_file in linklist_files:
                self._linklists[item_file.replace('.txt', '')] = item_file.replace('.txt', '')

            menu = self._link_list_option_menu['menu']
            menu.delete(0, 'end')

            for string in self._linklists:
                menu.add_command(label=string, command=lambda value=string: self.select(value))

        return self
