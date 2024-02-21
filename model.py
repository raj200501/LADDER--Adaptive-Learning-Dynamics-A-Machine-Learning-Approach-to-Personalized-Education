import merlin.models.tf as mm
import pandas as pd
from merlin.io import Dataset

# Assuming 'students.csv', 'questions.csv', and 'responses.csv' have been preprocessed
# and merged into a single DataFrame that is split into train and test sets.
# Let's call the merged DataFrame 'data'.

data = pd.read_csv('data.csv')  #git  This is your preprocessed and merged dataset

# Split the data into training and testing sets
# This is a placeholder; you'll need to split the data according to your needs.
train_set = data.sample(frac=0.8, random_state=123)  # for example, 80% for training
test_set = data.drop(train_set.index)

# Convert the Pandas DataFrames into Merlin Datasets
train = Dataset(train_set)
test = Dataset(test_set)

# Assuming 'train.schema' is defined based on the 'train' Dataset
# The schema should describe the structure of the input data for the model.

#merlin model NVIDIA
model = mm.DLRMModel(
    train.schema,  # The schema should be obtained from the 'train' dataset
    embedding_dim=64,
    bottom_block=mm.MLPBlock([128, 64]),
    top_block=mm.MLPBlock([128, 64, 32]),
    prediction_tasks=mm.BinaryClassificationTask(train.schema)
)

model.compile(optimizer="adagrad", run_eagerly=False)
model.fit(train, validation_data=test, batch_size=1024)
eval_metrics = model.evaluate(test, batch_size=1024, return_dict=True)

print(eval_metrics)
