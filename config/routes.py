from datagorri.controller.modeler import Modeler as ModelerController
from datagorri.controller.scraper import Scraper as ScraperController
from datagorri.view.modeler.modeler import Modeler as ModelerView
from datagorri.view.scraper.scraper import Scraper as ScraperView


routes = {
    'Modeler': {
        'controller': ModelerController(),
        'view': ModelerView
    },
    'Scraper': {
        'controller': ScraperController(),
        'view': ScraperView
    }
}

DEFAULT_ROUTE = 'Modeler'
