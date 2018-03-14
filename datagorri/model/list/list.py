from bs4 import BeautifulSoup
from datagorri.model.list.listelement import ListElement

class List:
    def __init__(self):
        self._index = ''
        self.type_index = ''
        self.html = ''
        self.elements = []
        self.child_lists = []
        self.css_classes = ''
        self.type = ''
        self.bs4 = None
        self._is_repetitive = True
        
    def get_index(self):
        return self._index
        
    def set_index(self, index):
        self._index = index
        return self
        
    def get_type_index(self):
        return self.type_index
        
    def set_type_index(self, index):
        self.type_index = index
        return self
        
    def get_html(self):
        return self.html
        
    def set_html(self, html):
        self.html = html
        
    def get_elements(self):
        return self.elements
        
    def set_elements(self, elems):
        self.elements = elems
        
    def get_child_lists(self):
        return self.child_lists
        
    def set_child_list(self, lists):
        self.child_lists = lists
        
    def get_css_classes(self):
        return self.css_classes
        
    def set_css_classes(self, css):
        self.css_classes = css
        
    def get_type(self):
        return self.type
        
    def set_type(self, type):
        self.type = type
        
    def as_bs4(self):
        return self.bs4
        
    def is_repetitive(self):
        return self._is_repetitive
        
    def set_repetitive(self, is_repetitive=True):
        self._is_repetitive = is_repetitive
        return self
        
    @staticmethod
    def create_from_html(html):
        list = List()
        list.set_html(html)
        
        list.bs4 = BeautifulSoup(html, 'html.parser')
        
        if list.bs4.has_attr('class'):
            list.set_css_classes(list.bs4['class'])
        
        # look for nested lists
        for index, xl in enumerate(list.bs4.find_all(["ol","ul","dl"])):
            if len(xl.find_parents(["ol","ul","dl"])) == 0:
                continue
            nestedList = List.create_from_html(str(xl))
            list.get_child_lists().append(nestedList)
        
        # get all elements (li, dt, dd)
        for index, li in enumerate(list.bs4.find_all(["li","dt","dd"])):
            # exclude list elements from nested lists
            if len(li.find_parents(["li","dt","dd"])) != 0:
                continue
            elem = ListElement.create_from_html(str(li))
            elem.set_index(len(list.get_elements()))
            list.get_elements().append(elem)
        
        return list