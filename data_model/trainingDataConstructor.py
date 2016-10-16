from labeled_data_readers.labelsReader import LabelsReader
from labeled_data_readers.sensorsObservationsReader import SensorsObservationsReader

import datetime
import csv
import sqlite3
import codecs
import os.path

LABELS_DIRECTORY = r'./datasets/Labelled/labels'
SENSORS_OBSERVATIONS_DIRECTORY = r'./datasets/Labelled/sensors'

class TrainingDataConstructor(object):
    def __init__(self, dbname):
        self.dbname = dbname
        self.labels_reader = LabelsReader(LABELS_DIRECTORY)
        self.sensors_observations_reader = SensorsObservationsReader(SENSORS_OBSERVATIONS_DIRECTORY)
        self.con = None

    def __del__(self):
        if self.con:
            self.con.close()

    def construct(self):
        if os.path.exists(self.dbname):
            return

        self.con = sqlite3.connect(self.dbname)

        labels_to_sensors_map = self.__mapLabelsToSensorsData()
        for nurseId_date, labeled_files in labels_to_sensors_map.items():
            self.__fillTables(labeled_files[0], labeled_files[1:])

    def __fillTables(self, labels_filename, sensors_data):
        cur = self.con.cursor()

        # in tables time is stored as text, because SQLite does not have datetime type
        # to operate with datetimes use SQLite built-in functions

        # id - unique number of the action row
        # action_name_id - id of the action from actions array read from acts.csv
        #                  and completed by adding action ids for those actions
        #                  that has a name but don;t have an id
        # start_t - start time of the action
        # finish_t - end time of the action
        cur.execute("CREATE TABLE IF NOT EXISTS "
                    "labeled_actions (id INTEGER UNIQUE NOT NULL PRIMARY KEY, "
                    "action_name_id INTEGER, start_t TEXT, finish_t TEXT);")

        with codecs.open(labels_filename, 'r', "utf-8") as f:
            csv_reader = csv.DictReader(f)
            csv_to_db = [(row['action_id'], row['action_name'], row['start_t'], row['finish_t']) for row in csv_reader]

        for item in csv_to_db:
            cur.execute("INSERT INTO labeled_actions (action_name_id, start_t, finish_t) VALUES (?, ?, ?);",
                        (self.labels_reader.addActionToActionsList(item[0], item[1]),
                        item[2], item[3]))

        # action_id - corresponding id of the action from labeled_actions
        # duration - time passed from the previous record in this table corresponding to this action_id
        cur.execute("CREATE TABLE IF NOT EXISTS "
                    "labeled_sensors (action_id INTEGER, duration TEXT,"
                     "chest_x REAL, chest_y REAL, chest_z REAL,"
                     "waist_x REAL, waist_y REAL, waist_z REAL,"
                     "right_x REAL, right_y REAL, right_z REAL,"
                     "FOREIGN KEY (action_id) REFERENCES labeled_actions(id));")

        for sensors_filename, start_time, end_time in sensors_data:
            prev_duration = None

            with open(sensors_filename,'rt') as f:
                csv_reader = csv.DictReader(f)
                csv_to_db = [(row['time'], row['chest_x'], row['chest_y'], row['chest_z'],
                          row['waist_x'], row['waist_y'], row['waist_z'],
                          row['right_x'], row['right_y'], row['right_z']) for row in csv_reader]

            for item in csv_to_db:
                time = [int(time_part) if time_part != '' else 0 for time_part in item[0].split('.')]
                duration = datetime.timedelta(seconds = time[0], milliseconds = time[1])
                cur_time = start_time + duration
                if not prev_duration:
                    prev_duration = duration

                cur.execute("SELECT id FROM labeled_actions "
                            "WHERE datetime(start_t) <= datetime(\'%s\') "
                            "AND datetime(finish_t) > datetime(\'%s\')" % (cur_time, cur_time))
                row = cur.fetchone()
                while row != None:
                    cur.execute("INSERT INTO labeled_sensors (action_id, duration,"
                                    "chest_x, chest_y, chest_z,"
                                    "waist_x, waist_y, waist_z,"
                                    "right_x, right_y, right_z)"
                                     " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                                (int(row[0]), str(duration - prev_duration),
                                 float(item[1]), float(item[2]), float(item[3]),
                                 float(item[4]), float(item[5]), float(item[6]),
                                 float(item[7]), float(item[8]), float(item[9])))
                    row = cur.fetchone()

                prev_duration = duration

        self.con.commit()

    def __mapLabelsToSensorsData(self):
        labels_data_files = self.labels_reader.getDataFiles()
        sensors_data_files = self.sensors_observations_reader.getDataFiles()

        # key of the dictionary is a pair (nurse_id, date)
        # value of the dictionary consists of the 1 labels file and 1 or more sensors files with date frame
        labels_to_sensors_map = dict()

        for f in labels_data_files:
            nurse_id, date = self.labels_reader.splitFileNameByPattern(f)
            labels_to_sensors_map[(nurse_id, date)] = [f]

        for f in sensors_data_files:
            nurse_id, date, start_time, end_time = self.sensors_observations_reader.splitFileNameByPattern(f)
            labels_to_sensors_map[(nurse_id, date)].append((f, start_time, end_time))

        return labels_to_sensors_map
