from os.path import exists
from os import environ
from typing import List
import logging
import joblib
import lightgbm as lgb
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

FORMAT = "%(asctime)s:%(name)s:%(levelname)s - %(message)s"
# Potentially log info during training.
logging.basicConfig(format=FORMAT, level=logging.INFO)

DATASET_PATH = environ["DATA_SOURCE"]
MODEL_OUTPUT_PATH = environ["OUTPUT_PATH"]

MODEL_NAME = "inspection-mo-regression-model.pickle"
ENCODER_NAME = "ord-enc.pickle"
SCALER_NAME = "standard_scaler.pickle"

DATASET_NAME = "inspections.csv"
DATASET_PREPROCESSED_NAME = "inspections_preprocessed.csv"

cache_preprocessing = False

def preprocess(features_categorical: List[str], features_embeddings: List[str], labels: List[str]) -> pd.DataFrame:
    
    """
    READ & TRANSFORM DATA
    """
    logging.info("READ & TRANSFORM DATA")
    inspections = pd.read_csv(f"{DATASET_PATH}/{DATASET_NAME}", delimiter=",")
    logging.info(f"TRAIN A MultiOutputRegressor USING {len(inspections)} RECORDS")

    inspections_processed = pd.DataFrame()
    """
    SCALE TARGETS
    """
    scaler: StandardScaler = StandardScaler()
    inspections_processed[labels] = scaler.fit_transform(inspections[labels].values)
    joblib.dump(scaler, open(f"{MODEL_OUTPUT_PATH}/{SCALER_NAME}", "wb"))

    """
    ENCODE CATEGORICAL FEATURES
    """
    logging.info("ENCODE CATEGORICAL FEATURES")
    ordincal_encoder: OrdinalEncoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
    inspections_processed[features_categorical] = ordincal_encoder.fit_transform(inspections[features_categorical].values)
    inspections_processed[features_categorical] = inspections_processed[features_categorical].astype('category')

    # Save the encoder to disk in the filesystem of the docker container.
    joblib.dump(ordincal_encoder, open(f"{MODEL_OUTPUT_PATH}/{ENCODER_NAME}", "wb"))

    """
    CALCULATE EMBEDDINGS
    """
    logging.info("CALCULATE EMBEDDINGS")
    sentence_transformer: SentenceTransformer = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1", cache_folder="/app/.cache")
    for feature in features_embeddings:
        feature_values = list(inspections[feature].values)
        embeddings = sentence_transformer.encode(feature_values)
        embedding_columns = [feature + f"_{str(i)}" for i in range(embeddings[0].shape[0])]
        inspections_processed = pd.concat([inspections_processed, pd.DataFrame(list(embeddings), columns=embedding_columns)], axis=1)
        
    return inspections_processed

def train(inspections_processed: pd.DataFrame, labels: List[str]):
    
    Y = inspections_processed[labels]
    X = inspections_processed.drop(labels, axis=1)
    
    regressor = lgb.LGBMRegressor()
    model: MultiOutputRegressor = MultiOutputRegressor(estimator=regressor)
    model.fit(X, Y)

    # Save the model to disk in the filesystem of the docker container.
    joblib.dump(model, open(f"{MODEL_OUTPUT_PATH}/{MODEL_NAME}", "wb"))

def run_workflow():
    FEATURES_CATEGORICAL = ["business_postal_code"]
    FEATURES_EMBEDDINGS = ["violation_description"]
    LABELS = ["inspection_score", "lowest_score"]
    
    """
    PREPROCESS / DATA LOADING
    """
    dataset_preprocessed_path = f"{DATASET_PATH}/{DATASET_PREPROCESSED_NAME}"
    if cache_preprocessing and exists(dataset_preprocessed_path):
        logging.info("LOAD PREPROCESSED DATA")
        inspections_processed: pd.DataFrame = pd.read_csv(dataset_preprocessed_path, delimiter=",")
    else:
        logging.info("PREPROCESS")
        inspections_processed: pd.DataFrame = preprocess(
            features_categorical=FEATURES_CATEGORICAL, 
            features_embeddings=FEATURES_EMBEDDINGS, 
            labels=LABELS
        )
        if cache_preprocessing:
            inspections_processed.to_csv(f"{DATASET_PATH}/{DATASET_PREPROCESSED_NAME}", index=False)
    
    """
    TRAIN
    """
    logging.info("TRAIN")
    train(inspections_processed, labels=LABELS)
    

if __name__ == "__main__":
    run_workflow()