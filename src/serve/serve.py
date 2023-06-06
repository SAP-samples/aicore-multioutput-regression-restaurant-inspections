from os.path import exists
from typing import List
import joblib
import pandas as pd
from flask import Flask, request
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

RESOURCE_GROUP = "restaurant-inspections"
MODEL_OUTPUT_PATH = "/mnt/models"
MODEL_NAME = "inspection-mo-regression-model.pickle"
ENCODER_NAME = "ord-enc.pickle"
SCALER_NAME = "standard_scaler.pickle"

sentence_transformer: SentenceTransformer = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1", cache_folder="/app/.cache")
multi_output_regressor: MultiOutputRegressor
ordinal_encoder: OrdinalEncoder
scaler: StandardScaler

@app.before_first_request
def init():
    """
    Load the model if it is available locally
    """
    global multi_output_regressor
    global ordinal_encoder
    global scaler

    MODEL_PATH = f"{MODEL_OUTPUT_PATH}/{MODEL_NAME}"
    ENCODER_PATH = f"{MODEL_OUTPUT_PATH}/{ENCODER_NAME}"
    SCALER_PATH = f"{MODEL_OUTPUT_PATH}/{SCALER_NAME}"

    if exists(MODEL_PATH):
        print(f"Loading multi-output regressor model from {MODEL_PATH}")
        multi_output_regressor = joblib.load(MODEL_PATH)
    else:
        raise FileNotFoundError(MODEL_PATH)

    if exists(ENCODER_PATH):
        print(f"Loading encoder model from {ENCODER_PATH}")
        ordinal_encoder = joblib.load(ENCODER_PATH)
    else:
        raise FileNotFoundError(ENCODER_PATH)

    if exists(SCALER_PATH):
        print(f"Loading scaler model from {SCALER_PATH}")
        scaler = joblib.load(SCALER_PATH)
    else:
        raise FileNotFoundError(SCALER_PATH)

def prepare_input_data(input_data: List) -> pd.DataFrame:
    FEATURES_CATEGORICAL = ["business_postal_code"]
    FEATURES_EMBEDDINGS = ["violation_description"]

    inspections = pd.DataFrame.from_records(input_data)
    inspections = inspections[["business_postal_code", "violation_description"]]

    inspections_processed = pd.DataFrame()

    """
    ENCODE CATEGORICAL FEATURES
    """
    print("ENCODE CATEGORICAL FEATURES")
    inspections_processed[FEATURES_CATEGORICAL] = ordinal_encoder.transform(inspections[FEATURES_CATEGORICAL].values)
    inspections_processed[FEATURES_CATEGORICAL] = inspections_processed[FEATURES_CATEGORICAL].astype('category')

    """
    CALCULATE EMBEDDINGS
    """
    print("CALCULATE EMBEDDINGS")
    for feature in FEATURES_EMBEDDINGS:
        feature_values = list(inspections[feature].values)
        embeddings = sentence_transformer.encode(feature_values)
        embedding_columns = [feature + f"_{str(i)}" for i in range(embeddings[0].shape[0])]
        inspections_processed = pd.concat([inspections_processed, pd.DataFrame(list(embeddings), columns=embedding_columns)], axis=1)
    
    return inspections_processed

@app.route("/v1/models/{}:predict".format(RESOURCE_GROUP), methods=["POST"])
def predict():
    "Make the model available for inference requests."
    data: pd.DataFrame = prepare_input_data(list(dict(request.json)["payload"]))  # type: ignore
    predictions_scaled = multi_output_regressor.predict(data.values)
    predictions = scaler.inverse_transform(predictions_scaled)
    response = {"predictions": predictions.tolist()}

    return response


if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0", debug=True, port=9001)