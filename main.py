from labeled_data_readers.labelsReader import LabelsReader
from labeled_data_readers.sensorsObservationsReader import SensorsObservationsReader

if __name__ == "__main__":
    labels_directory = r'./datasets/Labelled/labels'
    labels_reader = LabelsReader(labels_directory)
    labels_reader.load()

    sensors_observations_directory = r'./datasets/Labelled/sensors'
    sensors_observations_reader = SensorsObservationsReader(sensors_observations_directory)
    sensors_observations_reader.load()