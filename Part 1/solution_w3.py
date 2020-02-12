import sys


class FileReader:

    def __init__(self, file_name):
        self._file_name = file_name

    def read(self):
        try:
            f = open(self._file_name, "r")
            read_str = f.read()
            f.close()
            return read_str
        except IOError:
            return ""

if len(sys.argv)>1:
    reader = FileReader(sys.argv[1])
    print(reader.read())
