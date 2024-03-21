from utils.generator import NoteGenerator


class Writer:
    def __init__(self, output_file):
        self.output_file = output_file
        self.file = open(output_file, "w")
        self.file.write(self._get_header())

    def write(self, data: dict):
        generator = NoteGenerator(self)
        self.file.write(
            generator.generate(data['title'], data['content'], data['created'], data['updated'], data['tags'])
        )

    def close(self):
        self.file.write(self._get_footer())
        self.file.close()

    def _get_header(self):
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
<en-export export-date="20240321T052003Z" application="Evernote" version="10.80.3">"""

    def _get_footer(self):
        return "</en-export>"
