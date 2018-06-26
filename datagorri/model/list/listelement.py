from bs4 import BeautifulSoup


class ListElement:
    """
    Displays the Tags li, dt and dd.
    """
    def __init__(self):
        self._index = ''
        self.html = ''
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
                    "text": a.getText(),
                    "title": a['title'] if a.has_attr('title') else ''
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
                    "alt": img['alt'] if img.has_attr('alt') else '',
                    "title": img['title'] if img.has_attr('title') else ''
                })

        return images
    
    def get_html_lists(self):
        lists = []
        
        soup = self.as_bs4()
        for index, list in enumerate(soup.find_all(["ol","ul","dl"])):
            #skip if list has parent list
            if len(list.find_parents(["ol","ul","dl"])) != 0:
                continue
            lists.append(str(list))
            
        return lists
    
    @staticmethod
    def create_from_html(html):
        element = ListElement()
        element.set_html(html)
                
        element.bs4 = BeautifulSoup(html, 'html.parser')
        
        return element
        