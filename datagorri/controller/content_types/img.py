from datagorri.controller.content_types.content_type import ContentType


class Img(ContentType):
    """
    This class defines handling if the downloaded content was an image.

    """
    type = "Img"

    @staticmethod
    def is_applicable_to(col):
        return len(col.get_images()) > 0

    @staticmethod
    def get_content(col):
        returns = []

        for img_index, img in enumerate(col.get_images()):
            returns.append({
                'type': Img.type + 'Alt',
                'value': Img.get_alt_val(col, img_index),
                'img_index': img_index
            })
            returns.append({
                'type': Img.type + 'Src',
                'value': Img.get_src_val(col, img_index),
                'img_index': img_index
            })

        return returns

    @staticmethod
    def get_alt_val(col, img_index):
        images = col.get_images()
        if len(images) -1 < img_index:
            return False

        img = images[img_index]
        return img['alt'].strip().replace('\n', '').replace('\r', '')

    @staticmethod
    def get_src_val(col, img_index):
        images = col.get_images()
        if len(images) -1 < img_index:
            return False

        img = images[img_index]
        return img['src'].strip().replace('\n', '').replace('\r', '')
