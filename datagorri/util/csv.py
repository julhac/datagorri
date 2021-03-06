import csv
#from datagorri.controller.scraper import Scraper as Log

class Csv:
    """
    This class enables the handling of csv files.

    """
    @staticmethod
    def create_file(path, list_of_tables, list_of_lists, delimiter, encoding="UTF-8"):
        """
        This method takes a dictionary of data and saves it at a given path as csv file.

        :param path: (string) Save location
        :param list_of_tables: (dictionary) Data scraped from tables to save
        :param list_of_lists: (dictionary) Data scraped from lists to save
        :param delimiter: (string) the delimiter
        :return: -

        """
        # With Latin-1 encoding Excel displays the umlauts correct
        #with open(path, 'w', encoding='Latin-1') as f: # writing to file might crash due to unicode characters
        with open(path, 'w', encoding=encoding) as f:  # Excel has to import file in order to show umlauts correctly

            table_headers = []

            #write table data
            for entry in list_of_tables:
                for key, val in entry.items():
                    if key not in table_headers:
                        table_headers.append(key)

            writer = csv.DictWriter(f, fieldnames=table_headers, delimiter=delimiter)

            try:
                writer.writeheader()
                writer.writerows(list_of_tables)

            except Exception as e:
                print('file {}, {}'.format(path, e))
                return False
                #Log.update_log('Error writing file {}, {}'.format(path, e))

            list_headers = []

            #write list data
            for entry in list_of_lists:
                for key, val in entry.items():
                    if key not in list_headers:
                        list_headers.append(key)

            writer = csv.DictWriter(f, fieldnames=list_headers, delimiter=delimiter)
            
            try:
                writer.writeheader()
                writer.writerows(list_of_lists)

            except Exception as e:
                print('file {}, {}'.format(path, e))
                return False
                #Log.update_log('Error writing file {}, {}'.format(path, e))

            return True
    