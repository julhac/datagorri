from datagorri.controller.content_types.content_type import ContentType


class Text(ContentType):
    """
    This class defines handling if the downloaded content was basic text.

    """
    type = "Text"

    @staticmethod
    def is_applicable_to(col):
        return not Text.get_val(col).isspace()

    @staticmethod
    def get_content(col):
        return {
            'type': Text.type,
            'value': Text.get_val(col)
        }

    @staticmethod
    def get_val(col):
        return col.get_text().strip().replace('\n', '').replace('\r', '')
