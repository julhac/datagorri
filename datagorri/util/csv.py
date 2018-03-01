from unidecode import unidecode


class Csv:
    """
    This class enables the handling of csv files.

    """
    @staticmethod
    def create_file(path, list_to_save):
        """
        This method takes a dictionary of data and saves it at a given path as csv file.

        :param path: (string) Save location
        :param list_to_save: (dictionary) Data to save
        :return: -

        """

        # Maybe change to with open.. (no f.close() present)
        f = open(path, 'w')

        headers = []

        for entry in list_to_save:
            for key, val in entry.items():
                if not key in headers:
                    headers.append(key)

        headline = ";".join(headers) + '\n'
        f.write(headline)

        for entry in list_to_save:
            line = ''
            for header in headers:
                if header in entry:
                    line += entry[header]
                line += ';'

            try:
                line = unidecode(line)
                f.write(line + "\n")
            except Exception as e:
                print(e)
