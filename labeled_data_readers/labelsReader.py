from labeled_data_readers.actionsReader import*
from labeled_data_readers.reader import Reader

import os.path
import codecs
import datetime

class Label(object):
    def __init__(self, action_id, start_datetime, end_datetime):
        self.action_id = action_id
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

class LabelWrapper(object):
    def __init__(self, nurse_id, date, label):
        self.nurse_id = nurse_id
        self.date = date
        self.label = label

class LabelsReader(Reader):
    def __init__(self, directory):
        Reader.__init__(self, directory)
        self.labels = []

        actions_reader = ActionsReader(r'./datasets/Actions/')
        actions_reader.load()
        self.actions = actions_reader.actions

    def _loadFromFile(self, file_path):
        nurse_id, date = self._splitFileNameByPattern(file_path)

        rows=[]
        f = codecs.open(file_path, 'r', "utf-8")
        is_first_line = False
        for line in f:
            if not is_first_line:
                is_first_line = True
                continue

            line = line.rstrip()
            data = line.split(',');
            index = len(self.actions) + 1

            if not data[0]:
                does_index_exist = False
                for i in range(len(self.actions)):
                    # comparison does not pass
                    if data[1] == self.actions[i].action_string:
                        index = i + 1
                        does_index_exist = True
                        break

                if does_index_exist is False:
                    self.actions.append(Action(index, data[1]))
            else:
                index = int(data[0])

            start_datetime = datetime.datetime.strptime(data[2], "%Y-%m-%d %H:%M:%S")
            end_datetime = datetime.datetime.strptime(data[3], "%Y-%m-%d %H:%M:%S")

            rows.append(LabelWrapper(nurse_id, date, Label(index, start_datetime, end_datetime)))

        f.close()
        self.labels.extend(rows)

    # labels file name pattern is the next:
    # N0xx_YYYYMMDD
    # xx - nurse_id
    # YYYYMMDD - date
    def _splitFileNameByPattern(self, path):
        file_name_with_ext = os.path.basename(path)
        file_name = os.path.splitext(file_name_with_ext)[0]
        nurse_id_and_date = file_name.split('_')
        nurse_id = int(nurse_id_and_date[0][1:])
        date = datetime.datetime.strptime(nurse_id_and_date[1], "%Y%m%d")
        return nurse_id, date
