# Inspect Training and Serving implementation

First the model needs to be trained using the inspections training
data. Then one can serve the model to predict the *overall inspection score* and the *lowest
partial score* based on new data about an inspection.

To take a look at the training in full detail you can find the code [here](). The code for
serving the model is available [here](../src/train/train.py).
 
In order to increase the quality of the training one first *preprocesses* the data of the inspections.

## Data Preprocessing

The data preprocessing includes the following steps in sequential order:
 
1. Scale the targets/labels which in this case are the inspection score and the lowest
   partial score
2. Use an
   [ordinal encoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OrdinalEncoder.html)
   to encode the business postal codes to numerical values
3. Leverage [SBERT](https://www.sbert.net/) (Sentence-BERT) to create an embedding for each text description of violations. An embedding here is a multidimensional,
continuous vector that represents the semantics of the text description.
4. For each dimension of the embedding create a separate column that holds the numerical value of
that dimension of the vector

## Model Training

The model is later on supposed to predict two targets, the inspection score and the lowest
partial score. To do so one trains two [LightGBM](https://lightgbm.readthedocs.io/en/v3.3.2/) regressors in parallel, one for each
target variable. The two regressors can than be abstracted to a so called
[Multi-Output-Regressor](https://scikit-learn.org/stable/modules/generated/sklearn.multioutput.MultiOutputRegressor.html) model.
This then acts as an additional abstraction layer for both regressors. It can predict both target variables at the same time. 
 
## Model Serving

[Flask](https://flask.palletsprojects.com/en/2.2.x/) is used as a web server in order to expose the model through an endpoint. A client
can then can send requests to that endpoint. Once it receives a request that contains data about a
new inspection, the model predicts the overall inspection score and the lowest partial
score. Finally, the web server returns the predicted scores as response back to the
client.
 
Training the model and serving the model both run inside Docker containers in the cloud
using AI Core.