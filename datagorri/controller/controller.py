"""
.. module:: controller
"""

from abc import abstractmethod
from config.app import config
from datagorri.util.json import Json

class Controller:
    def __init__(self):
        self.view = None
        pass

    @abstractmethod
    def on_route(self, view_class, master_frame):
        pass

    @staticmethod
    def load_page_model(file):
        """
        Loads the page model from the given file. Error handling has to be done by the caller

        :params file: path to the page model file
        :returns: (dict or False) dict representing the content of the json file
        """
        return Json.load_json_file(file)        