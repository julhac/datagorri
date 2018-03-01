from datagorri.controller.content_types.content_type import ContentType


class Link(ContentType):
    """
    This class defines handling if the downloaded content was a link. Inherited from ContentType.

    """
    type = "Link"

    @staticmethod
    def is_applicable_to(col):
        """
        Returns True if the column contains a link otherwise False
        :param col: (Column) the column
        :return: (boolean)

        """
        return len(col.get_links()) > 0

    @staticmethod
    def get_content(col):
        """
        Returns the content of a column in a list links
        :param col: (Column) the column
        :return: (list)

        """
        returns = []

        for link_index, link in enumerate(col.get_links()):
            returns.append({
                'type': Link.type,
                'value': Link.get_href_val(col, link_index),
                'link_index': link_index
            })

            if not link['text'] == '':
                returns.append({
                    'type': Link.type + 'Text',
                    'value': Link.get_text_val(col, link_index),
                    'link_index': link_index
                })

        return returns

    @staticmethod
    def get_text_val(col, link_index):
        """
        Returns the to a link corresponding text value or False if the value is not available
        :param col: (Column) the column
        :param link_index: (int) position of the link
        :return: (string or False)

        """
        links = col.get_links()
        if len(links) - 1 < link_index:
            return False

        link = links[link_index]
        return link['text'].strip().replace('\n', '').replace('\r', '')

    @staticmethod
    def get_href_val(col, link_index):
        """
        Returns the to a link corresponding href value or False if the value is not available
        :param col:  (Column) the column
        :param link_index: (int) position of the link
        :return: (string or False)

        """
        links = col.get_links()
        if len(links) - 1 < link_index:
            return False

        link = links[link_index]
        return link['href'].strip().replace('\n', '').replace('\r', '')
