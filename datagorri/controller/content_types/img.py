from datagorri.controller.content_types.content_type import ContentType


class Img(ContentType):
    """
    This class defines handling if the downloaded content was an image. Inherited from ContentType.

    """
    type = "Img"

    @staticmethod
    def is_applicable_to(tag):
        """
        Returns True or False depending of the column contains images.

        :param tag: (Column or ListElement) the column or list element
        :return: (boolean)
        """
        return len(tag.get_images()) > 0

    @staticmethod
    def get_content(tag):
        """
        Returns the content of Images of a column in a list
        :param tag: (Column or ListElement) the column or list element
        :return: (list)
        """
        returns = []

        for img_index, img in enumerate(tag.get_images()):
            returns.append({
                'index': tag.get_index(),
                'type': Img.type + 'Alt',
                'value': Img.get_alt_val(tag, img_index),
                'img_index': img_index
            })
            returns.append({
                'index': tag.get_index(),
                'type': Img.type + 'Src',
                'value': Img.get_src_val(tag, img_index),
                'img_index': img_index
            })

        return returns

    @staticmethod
    def get_alt_val(tag, img_index):
        """
        Returns the alternative string of an image or False
        :param tag: (Column or ListElement) the column or list element
        :param img_index: (int) the number index in the column
        :return: (string or False)
        """
        images = tag.get_images()
        if len(images) -1 < img_index:
            return False

        img = images[img_index]
        return img['alt'].strip().replace('\n', '').replace('\r', '')

    @staticmethod
    def get_src_val(tag, img_index):
        """
        Returns the source url of an image or False
        :param tag: (Column or ListElement) the column or list element
        :param img_index: (int) the number index in the column
        :return: (string or False)
        """
        images = tag.get_images()
        if len(images) - 1 < img_index:
            return False

        img = images[img_index]
        return img['src'].strip().replace('\n', '').replace('\r', '')
