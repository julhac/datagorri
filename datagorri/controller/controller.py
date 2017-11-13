from abc import abstractmethod


class Controller:
    def __init__(self):
        self.view = None
        pass

    @abstractmethod
    def on_route(self, view_class, master_frame):
        pass
