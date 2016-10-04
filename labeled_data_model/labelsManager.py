from labeled_data_model.actionsReader import Action

import os.path
import codecs
import datetime

class Label(object):
    def __init__(self, nurse_id, date, action_id, start_time, end_time):
        self.nurse_id = nurse_id
        self.date = date
        self.action_id = action_id
        self.start_time = start_time
        self.end_time = end_time

class LabelsManager(object):
    def __init__(self, labels_dir, actions):
        self.labels_dir = labels_dir
        self.actions = actions
        self.labels = []

    def loadLabels(self):
        labels_files = []

        for root, dirs, files in os.walk(self.labels_dir):
            for f in files:
                fullpath = os.path.join(root, f)
                if os.path.splitext(fullpath)[1] == '.csv':
                    labels_files.append(fullpath)

        for f in labels_files:
            self.labels.extend(self.__loadLabelsFromFile(f))

    def __loadLabelsFromFile(self, filename):
        nurse_id, date = self.__splitFileNameByPattern(filename)

        rows=[]
        f = codecs.open(filename, 'r', "utf-8")
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
                index = data[0]

            start_time = datetime.datetime.strptime(data[2], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(data[3], "%Y-%m-%d %H:%M:%S")

            rows.append(Label(nurse_id, date, index, start_time, end_time))

        f.close()
        return rows

    # in labeled data file name pattern is the next:
    # N0xx_YYYYMMDD
    # xx - nurse_id
    # YYYYMMDD - date
    def __splitFileNameByPattern(self, path):
        file_name_with_ext = os.path.basename(path)
        file_name = os.path.splitext(file_name_with_ext)[0]
        nurse_id_and_date = file_name.split('_')
        nurse_id = int(nurse_id_and_date[0][1:])
        date = datetime.datetime.strptime(nurse_id_and_date[1], "%Y%m%d")
        return nurse_id, date
