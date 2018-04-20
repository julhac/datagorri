from datagorri.controller.content_types.content_type import ContentType


class Text(ContentType):
    """
    This class defines handling if the downloaded content was basic text. Inherited from ContentType.

    """
    type = "Text"

    @staticmethod
    def is_applicable_to(tag):
        """
        Returns True or False depending if the column value is empty

        :param tag: (Column or ListElement) the column or list element
        :return: (boolean)

        """
        return not Text.get_val(tag).isspace()

    @staticmethod
    def get_content(tag):
        """
        Returns the type and value of a column

        :param tag: (Column or ListElement) the column or list element
        :return: (dict) type and value

        """
        return {
            'index': tag.get_index(),
            'type': Text.type,
            'value': Text.get_val(tag)
        }

    @staticmethod
    def get_val(tag):
        """
        Returns the value of a column

        :param tag: (Column or ListElement) the column or list element
        :return: (string) the stripped value

        """
        return tag.get_text().strip().replace('\n', '').replace('\r', '')
