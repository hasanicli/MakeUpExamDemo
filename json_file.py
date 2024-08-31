import json


class JsonFile:
    @staticmethod
    def read(file_path):
        with open(file_path, "a+", encoding="utf-8") as file_object:
            try:
                file_object.seek(0)
                data = json.load(file_object)
            except Exception:
                data = []
            return data

    @staticmethod
    def write(file_path, data):
        with open(file_path, "w", encoding="utf-8") as file_object:
            file_object.write(json.dumps(data, ensure_ascii=False, indent=4))
