from labeled_data_readers.reader import Reader

import codecs
import re

class Action(object):
    def __init__(self, id, action_string):
        self.id = id
        self.action_string = action_string

class ActionsReader(Reader):
    def __init__(self, directory):
        Reader.__init__(self, directory)
        self.actions = []

    def _loadFromFile(self, file_path):
        actions = []
        f = codecs.open(file_path, 'r', 'utf-8')
        is_first_line = False
        for line in f:
            if not is_first_line:
                is_first_line = True
                continue

            data = line.split(',');
            action_string = self.__getTextInQuotes(data[1])
            actions.append(Action(int(data[0]), action_string))

        f.close()
        self.actions.extend(actions)

    def __getTextInQuotes(self, text):
        res = re.findall('\"(.*?)\"', text)
        return res[0]
