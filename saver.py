import json


class OutputWriter:
    def __init__(self, path, converter):
        self.converter = converter
        self.path = path
        self.data = []

    def write(self, data):
        self.data += self.converter(data)

    def __enter__(self):
        self.file = open(self.path, 'w', encoding="utf8")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        json.dump(self.data, self.file)
        self.file.close()
