from unidecode import unidecode

class Csv:
    @staticmethod
    def create_file(path, list_to_save):
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