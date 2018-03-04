import csv


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
        # With Latin-1 encoding Excel displays the umlauts correct
        with open(path, 'w', encoding='Latin-1') as f:

            headers = []

            for entry in list_to_save:
                for key, val in entry.items():
                    if key not in headers:
                        headers.append(key)

            writer = csv.DictWriter(f, fieldnames=headers, delimiter=';')

            try:
                writer.writeheader()
                writer.writerows(list_to_save)

            except Exception as e:
                print('file {}, {}'.format(path, e))

