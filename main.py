from labeled_data_model.actionsReader import ActionsReader
from labeled_data_model.labelsManager import LabelsManager

if __name__ == "__main__":
    actions_reader = ActionsReader()

    labels_directory = r'./datasets/Labelled/labels'
    labels_manager = LabelsManager(labels_directory, actions_reader.loadActions(r'./datasets/acts.csv'))
    labels_manager.loadLabels()