from datagorri.controller.content_types.content_type import ContentType


class Link(ContentType):
    """
    This class defines handling if the downloaded content was a link. Inherited from ContentType.

    """
    type = "Link"

    @staticmethod
    def is_applicable_to(tag):
        """
        Returns True if the column contains a link otherwise False

        :param tag: (Column or ListElement) the column or list element
        :return: (boolean)

        """
        return len(tag.get_links()) > 0

    @staticmethod
    def get_content(tag):
        """
        Returns the content of a column in a list links

        :param tag: (Column or ListElement) the column or list element
        :return: (list)

        """
        returns = []

        for link_index, link in enumerate(tag.get_links()):
            returns.append({
                'index': tag.get_index(),
                'type': Link.type,
                'value': Link.get_href_val(tag, link_index),
                'link_index': link_index
            })

            if not link['text'] == '':
                returns.append({
                    'index': tag.get_index(),
                    'type': Link.type + 'Text',
                    'value': Link.get_text_val(tag, link_index),
                    'link_index': link_index
                })

        return returns

    @staticmethod
    def get_text_val(tag, link_index):
        """
        Returns the to a link corresponding text value or False if the value is not available

        :param tag: (Column or ListElement) the column or list element
        :param link_index: (int) position of the link
        :return: (string or False)

        """
        links = tag.get_links()
        if len(links) - 1 < link_index:
            return False

        link = links[link_index]
        return link['text'].strip().replace('\n', '').replace('\r', '')

    @staticmethod
    def get_href_val(tag, link_index):
        """
        Returns the to a link corresponding href value or False if the value is not available

        :param tag: (Column or ListElement) the column or list element
        :param link_index: (int) position of the link
        :return: (string or False)

        """
        links = tag.get_links()
        if len(links) - 1 < link_index:
            return False

        link = links[link_index]
        return link['href'].strip().replace('\n', '').replace('\r', '')
