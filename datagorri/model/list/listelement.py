from bs4 import BeautifulSoup

class ListElement:
    def __init__(self):
        self._index = ''
        self.html = ''
        self.child_lists = []
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
     
    def get_child_lists(self):
        return self.child_lists
        
    def set_child_list(self, lists):
        self.child_lists = lists
        
    def as_bs4(self):
        return self.bs4
        
    def get_text(self):
        return self.bs4.getText().strip().replace('  ', ' ')
        
    def has_link(self):
        # look for links in lists
        for index, a in enumerate(self.as_bs4().find_all("a")):
            if len(a.find_parents("ol")) != 0 or len(a.find_parents("ul")) != 0:
                continue

            if a.has_attr('href'):
                return True

        return False

    def get_links(self):
        links = []

        for index, a in enumerate(self.as_bs4().find_all("a")):
            if len(a.find_parents("ol")) != 0 or len(a.find_parents("ul")) != 0:
                continue

            if a.has_attr('href'):
                links.append({
                    "href": a['href'],
                    "text": a.getText()
                })

        return links

    def get_images(self):
        images = []

        for index, img in enumerate(self.as_bs4().find_all("img")):
            if len(img.find_parents("ol")) != 0 or len(img.find_parents("ul")) != 0:
                continue

            if img.has_attr('src') or img.has_attr('alt'):
                images.append({
                    "src": img['src'] if img.has_attr('src') else '',
                    "alt": img['alt'] if img.has_attr('alt') else ''
                })

        return images
        
    @staticmethod
    def create_from_html(html):
        element = ListElement()
        element.set_html(html)
                
        element.bs4 = BeautifulSoup(html, 'html.parser')
        
        for index, ol in enumerate(element.bs4.find_all("ol")):
            if len(ol.find_parents("ol")) == 0:
                continue
            nestedList = List.create_from_html(str(ol))
            element.get_child_lists().append(nestedList)
            
        for index, ul in enumerate(element.bs4.find_all("ul")):
            if len(ul.find_parents("ul")) == 0:
                continue
            nestedList = List.create_from_html(str(ul))
            element.get_child_lists().append(nestedList)
        
        return element