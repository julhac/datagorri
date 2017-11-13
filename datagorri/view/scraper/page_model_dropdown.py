import tkinter
from datagorri.view.component import Component
from datagorri.view.style.scraper import style
from datagorri.controller.scraper import Scraper as ScraperController
from datagorri.controller.modeler import Modeler as ModelerController


style = style['page_model_dropdown']


class PageModelDropDown(Component):
    def __init__(self, master_frame):
        Component.__init__(self, master_frame)

        self._selected = tkinter.StringVar(master_frame)
        self.no_pms_label = None

        self._models = dict()
        pm_files = ScraperController.get_page_models()
        for pm_file in pm_files:
            self._models[pm_file.replace('.json','')] = pm_file.replace('.json','')

        if len(self._models.keys()) < 1:
            self._models[""] = ""

        len_longest_model_name = len(max(pm_files,"                                          ", key=len))

        self._page_model_option_menu = tkinter.OptionMenu(self.get_frame(), self._selected, *self._models.keys())
        self._page_model_option_menu.config(width=len_longest_model_name)
        self._page_model_option_menu.configure(bg=style['bg'])

        if len(pm_files) > 0:
            self._page_model_option_menu.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        else:
            self.no_pms_label = tkinter.Label(self.get_frame(), text="Create a page model first!", bg=style['bg'])
            self.no_pms_label.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

        self.select("select the page model to use")
        ModelerController.dropdown_to_update=self

    def select(self, name):
        self._selected.set(name)
        return self

    def get_selected(self):
        return self._selected.get()

    def get_all(self):
        models = []
        for page_model in self._models:
            if page_model is not None:
                models.append(page_model)

        return models

    def refresh(self):
        if self.no_pms_label is not None:
            self._models = {}
            self.no_pms_label.destroy()
            self._page_model_option_menu.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
            self.no_pms_label = None

        pm_files = ScraperController.get_page_models()
        for item_file in pm_files:
            self._models[item_file.replace('.json','')] = item_file.replace('.json','')

        menu = self._page_model_option_menu["menu"]
        menu.delete(0,"end")
        for string in self._models:
            menu.add_command(label=string,command=lambda value=string: self._selected.set(value))
