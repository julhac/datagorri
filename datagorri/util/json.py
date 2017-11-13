import json


class Json:
    @staticmethod
    def create_file(path, dict_to_save):
        j = json.dumps(dict_to_save, indent=4, ensure_ascii=False)
        f = open(path, 'w+')
        f.write(j)
        f.close()

    @staticmethod
    def load_json_file(path):
        try:
            return json.load(open(path))
        except FileNotFoundError:
            return False
