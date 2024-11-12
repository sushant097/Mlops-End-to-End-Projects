import pandas as pd
import pickle
from sklearn.metrics import accuracy_score
import yaml
from sklearn.metrics import accuracy_score
import yaml
import os
import mlflow
from urllib.parse import urlparse

import mlflow
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()


# load variables
# Set MLflow tracking URI
os.environ["MLFLOW_TRACKING_URI"] = os.getenv("MLFLOW_TRACKING_URI")
os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("REPO_OWNER")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_TRACKING_PASSWORD")


# load the parameters from yaml file
params = yaml.safe_load(open("params.yaml"))["train"]

def evaluate(data_path, model_path):
    data = pd.read_csv(data_path)
    X = data.drop(columns=["Outcome"])
    y = data["Outcome"]

    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

    ## load the model from the disk
    model = pickle.load(open(model_path, 'rb'))

    predictions = model.predict(X)
    accuracy_value = accuracy_score(y, predictions)

    # log metrics to mlflow
    mlflow.log_metric("accuracy", accuracy_value)
    print(f"MOdel accuracy:{accuracy_value} ")


if __name__ == "__main__":
    evaluate(params["data"], params["model"])
