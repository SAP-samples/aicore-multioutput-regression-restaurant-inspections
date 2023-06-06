# Adjust implementation to your Data

Feel free to make adjustments to use your own dataset instead of the
inspections dataset used throughout this mission.

In case your dataset is very similar to it and you are going to use the same
python libraries, do the following:

- Upload your own dataset to the same Amazon S3 bucket
- Inside the *train.py* file one uses for training, add the feature names and label names from your dataset to the
  according lists at the beginning of the *run_workflow* file. For example the name of
  a categorical feature goes into the `FEATURES_CATEGORICAL` list. Do the same for the
  lists of feature names in the serving.py file.
- Still in *train.py*, make sure to change the value of the `DATASET_NAME` variable to the name of the
  dataset that you uploaded to the S3 bucket in the previous step.

You can find more general instructions on how to adjust the repository of this
mission to your use case [here](https://github.com/kay-schmitteckert/aicore-multioutput-regression-restaurant-inspections/tree/mission#boilerplate-ai-core).
