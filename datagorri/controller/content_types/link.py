from datagorri.controller.content_types.content_type import ContentType


class Link(ContentType):
    """
    This class defines handling if the downloaded content was a link.

    """
    type = "Link"

    @staticmethod
    def is_applicable_to(col):
        return len(col.get_links()) > 0

    @staticmethod
    def get_content(col):
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
        links = col.get_links()
        if len(links) - 1 < link_index:
            return False

        link = links[link_index]
        return link['text'].strip().replace('\n', '').replace('\r', '')

    @staticmethod
    def get_href_val(col, link_index):
        links = col.get_links()
        if len(links) - 1 < link_index:
            return False

        link = links[link_index]
        return link['href'].strip().replace('\n', '').replace('\r', '')
