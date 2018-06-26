from bs4 import BeautifulSoup
from datagorri.model.list.list import List
from datagorri.model.list.listelement import ListElement


class Nestedlist(List):
    def __init__(self, index, parent_index, parent_element_index):
        List.__init__(self)
        self.set_index(index)
        self._parent_index = parent_index
        self._parent_element_index = parent_element_index
        
    def get_parent_index(self):
        return self._parent_index
        
    def get_parent_element_index(self):
        return self._parent_element_index
        
    @staticmethod
    def create_from_html(html, index, parent_index, parent_element_index):
        list = Nestedlist(index, parent_index, parent_element_index)
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