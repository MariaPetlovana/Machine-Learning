import os.path
import re
import codecs
import datetime

class Action(object):
    def __init__(self, id, action_string):
        self.id = id
        self.action_string = action_string

class ActionsManager(object):
    def __getTextInQuotes(self, text):
        res = re.findall('\"(.*?)\"', text)
        return res[0]

    def loadActions(self, filename):
        actions = []
        f = codecs.open(filename, 'r', 'utf-8')
        is_first_line = False
        for line in f:
            if not is_first_line:
                is_first_line = True
                continue

            data = line.split(',');
            action_string = self.__getTextInQuotes(data[1])
            actions.append(Action(int(data[0]), action_string))

        f.close()
        return actions

class Label(object):
    def __init__(self, id, date_start, date_end):
        self.id = id
        self.date_start = date_start
        self.date_end = date_end

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
            self.labels.extend(self.loadLabelsFromFile(f))

    def loadLabelsFromFile(self, filename):
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

            rows.append(Label(index, start_time, end_time))

        f.close()
        return rows

if __name__ == "__main__":
    actions_manager = ActionsManager()

    labels_directory = r'./datasets/Labelled/labels'
    labels_manager = LabelsManager(labels_directory, actions_manager.loadActions(r'./datasets/acts.csv'))
    labels_manager.loadLabels()