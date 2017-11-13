from config.app import config
from datagorri.view import Gui
from datagorri.router import Router
from config.routes import routes, DEFAULT_ROUTE
import os
from sys import platform


class App:
    def __init__(self):
        App.init_working_dirs()

        self._gui = Gui(config['title'], full_screen=config['full_screen'])
        self._gui.get_nav().add(list(routes.keys()))

        self._router = Router(self._gui.get_master_frame_of_views(), routes)
        self._gui.get_nav().on_click(lambda route: self._router.route(route))

        # show default page
        self._gui.get_nav().click_at(DEFAULT_ROUTE)

        self._gui.view()

    @staticmethod
    def init_working_dirs():
        if platform == "win32" or platform == "darwin":
            homepath = os.path.expanduser("~")
            os.chdir(homepath)

            if not os.path.exists("Desktop"):
                os.makedirs("Desktop")

            os.chdir(homepath + "/Desktop")

            if not os.path.exists("DataGorri_Output"):
                os.makedirs("DataGorri_Output")

            working_dir = homepath + "/Desktop/DataGorri_Output/"
            os.chdir(working_dir)

            if not os.path.exists("models"):
                os.makedirs("models")

            if not os.path.exists("results"):
                os.makedirs("results")

            if not os.path.exists("link_lists"):
                os.makedirs("link_lists")

            os.chdir(working_dir)

        return True
