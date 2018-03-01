from datagorri.controller.content_types.content_type import ContentType


class Text(ContentType):
    """
    This class defines handling if the downloaded content was basic text. Inherited from ContentType.

    """
    type = "Text"

    @staticmethod
    def is_applicable_to(col):
        """
        Returns True or False depending if the column value is empty
        :param col: (Column) the column
        :return: (boolean)

        """
        return not Text.get_val(col).isspace()

    @staticmethod
    def get_content(col):
        """
        Returns the type and value of a column
        :param col: (Column) the column
        :return: (dict) type and value

        """
        return {
            'type': Text.type,
            'value': Text.get_val(col)
        }

    @staticmethod
    def get_val(col):
        """
        Returns the value of a column
        :param col: (Column) the column
        :return: (string) the stripped value

        """
        return col.get_text().strip().replace('\n', '').replace('\r', '')
