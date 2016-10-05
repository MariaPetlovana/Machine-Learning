import os.path

class Reader(object):
    # directory - path from which data will be loaded
    def __init__(self, directory):
        self.directory = directory

    def load(self):
        files_to_read = []

        for root, dirs, files in os.walk(self.directory):
            for f in files:
                fullpath = os.path.join(root, f)
                if os.path.splitext(fullpath)[1] == '.csv':
                    files_to_read.append(fullpath)

        for f in files_to_read:
            self._loadFromFile(f)

    # should be reimplemented in descendants
    def _loadFromFile(self, file_path):
        return

    def _splitFileNameByPattern(self, path):
        return
