import json


class Json:
    """
    This class enables content handling in the Json format.

    """
    @staticmethod
    def create_file(path, dict_to_save):
        """
        This method saves a dictionary at the provided location as json file.

        :param path: (string) path to save the file
        :param dict_to_save: (dictionary)
        :return: -

        """
        j = json.dumps(dict_to_save, indent=4, ensure_ascii=False)
        f = open(path, 'w+')  # Maybe change to with open...
        f.write(j)
        f.close()

    @staticmethod
    def load_json_file(path):
        """
        This method tries to load a specified Json file.

        """
        try:
            return json.load(open(path))
        except FileNotFoundError:
            return False
