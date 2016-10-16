from labeled_data_readers.reader import Reader

import os.path
import codecs
import datetime

class Coordinates(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class SensorObservation(object):
    def __init__(self, time_delta, chest_pos, waist_pos, right_pos):
        self.time_delta = time_delta
        self.chest_pos = chest_pos
        self.waist_pos = waist_pos
        self.right_pos = right_pos

class SensorObservationWrapper(object):
    def __init__(self, nurse_id, date, start_time, end_time, sensor_observation):
        self.nurse_id = nurse_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.sensor_observation = sensor_observation

class SensorsObservationsReader(Reader):
    def __init__(self, directory):
        Reader.__init__(self, directory)
        self.sensors_observations = []

    def _loadFromFile(self, file_path):
        nurse_id, date, start_time, end_time = self._splitFileNameByPattern(file_path)

        rows=[]
        f = codecs.open(file_path, 'r', "utf-8")
        is_first_line = False
        for line in f:
            if not is_first_line:
                is_first_line = True
                continue

            line = line.rstrip()
            data = line.split(',');

            time_delta = float(data[0])

            chest_x = float(data[1])
            chest_y = float(data[2])
            chest_z = float(data[3])

            waist_x = float(data[4])
            waist_y = float(data[5])
            waist_z = float(data[6])

            right_x = float(data[7])
            right_y = float(data[8])
            right_z = float(data[9])

            rows.append(
                SensorObservationWrapper(
                    nurse_id,
                    date,
                    start_time,
                    end_time,
                    SensorObservation(
                        time_delta,
                        Coordinates(chest_x, chest_y, chest_z),
                        Coordinates(waist_x, waist_y, waist_z),
                        Coordinates(right_x, right_y, right_z)
                    )
                )
            )

        f.close()
        self.sensors_observations.extend(rows)

    # sensors file name pattern is the next:
    # N0xx_YYYYMMDD_HHMMSS-HHMMSS
    # xx - nurse_id
    # YYYYMMDD - date
    # HHMMSS - time
    def splitFileNameByPattern(self, path):
        file_name_with_ext = os.path.basename(path)
        file_name = os.path.splitext(file_name_with_ext)[0]
        splitted_filename = file_name.split('_')
        nurse_id = int(splitted_filename[0][1:])
        date = datetime.datetime.strptime(splitted_filename[1], "%Y%m%d")
        time_start_and_end = splitted_filename[2].split('-')
        start_time = datetime.datetime.strptime(time_start_and_end[0], "%H%M%S")
        start_time = start_time.replace(year = date.year, month = date.month, day = date.day)
        end_time = datetime.datetime.strptime(time_start_and_end[1], "%H%M%S")
        end_time = end_time.replace(year = date.year, month = date.month, day = date.day)
        return nurse_id, date, start_time, end_time
