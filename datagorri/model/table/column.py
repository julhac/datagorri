from bs4 import BeautifulSoup


class Column:
    def __init__(self):
        self._index = ''
        self.html = ''
        self.bs4 = None

    def __str__(self):
        return str(self.get_html())

    def get_index(self):
        return self._index

    def set_index(self, index):
        self._index = index

    def get_html(self):
        return self.html

    def set_html(self, html):
        self.html = html

    def as_bs4(self):
        return self.bs4

    def get_text(self):
        return self.bs4.getText().strip().replace('  ', ' ')

    def has_link(self):
        # look for table headers
        for index, a in enumerate(self.as_bs4().find_all("a")):
            if len(a.find_parents("table")) != 0:
                continue

            if a.has_attr('href'):
                return True

        return False

    def get_links(self):
        links = []

        for index, a in enumerate(self.as_bs4().find_all("a")):
            if len(a.find_parents("table")) != 0:
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
            if len(img.find_parents("table")) != 0:
                continue

            if img.has_attr('src') or img.has_attr('alt'):
                images.append({
                    "src": img['src'] if img.has_attr('src') else '',
                    "alt": img['alt'] if img.has_attr('alt') else ''
                })

        return images

    def get_html_tables(self):
        tables = []

        soup = self.as_bs4()
        for index, table in enumerate(soup.find_all("table")):
            # skip if table has parent table
            if len(table.find_parents("table")) != 0:
                continue

            tables.append(str(table))

        return tables

    @staticmethod
    def create_from_html(html):
        col = Column()
        col.set_html(html)

        col.bs4 = BeautifulSoup(html, 'html.parser')

        return col
