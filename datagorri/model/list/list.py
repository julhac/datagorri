from bs4 import BeautifulSoup
from datagorri.model.list.listelement import ListElement

class List:
    def __init__(self):
        self._index = ''
        self.html = ''
        self.elements = []
        self.css_classes = ''
        self.bs4 = None
        
    def get_index(self):
        return self._index
        
    def set_index(self, index):
        self._index = index
        return self
        
    def get_html(self):
        return self.html
       
    def set_html(self, html):
        self.html = html
        
    def get_elements(self):
        return self.elements
        
    def set_elements(self, elems):
        self.elements = elems
        
    def get_css_classes(self):
        return self.css_classes
        
    def set_css_classes(self, css):
        self.css_classes = css
        
    def as_bs4(self):
        return self.bs4
        
    @staticmethod
    def create_from_html(html):
        list = List()
        list.set_html(html)
        
        list.bs4 = BeautifulSoup(html, 'html.parser')
        
        if list.bs4.has_attr('class'):
            list.set_css_classes(list.bs4['class'])
            
        # get all elements (li)
        for index, li in enumerate(list.bs4.find_all("li")):
            elem = ListElement.create_from_html(str(li))
            elem.set_index(len(list.get_elements()))
            list.get_elements().append(elem)
            
        return list