from data_model.trainingDataConstructor import TrainingDataConstructor

DB_NAME = 'training_data.db'

if __name__ == "__main__":
    training_data_ctor = TrainingDataConstructor(DB_NAME)
    training_data_ctor.construct()
