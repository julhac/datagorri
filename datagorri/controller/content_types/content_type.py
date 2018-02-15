class ContentType:
    """
    The base class for content. To allow a fine grained distinction
    the different content types inherit from this class.
    """
    type = "ContentType"

    @staticmethod
    def is_applicable_to(col):
        return

    @staticmethod
    def get_content(col):
        return
