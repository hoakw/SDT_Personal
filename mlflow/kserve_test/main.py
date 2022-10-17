import kserve
from typing import Dict
import os
import warnings
import sys
import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature


class Kserve_model(kserve.Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.ready = False 

    def predict(self, request: Dict) -> Dict:

        minio_host = "mlflow-minio.mlflow-system.svc.cluster.local"
        mlflow_host = "mlflow-service.mlflow-system.svc.cluster.local"
        model_name1 = "serving_test"
        mlflow.set_tracking_uri(f'http://{mlflow_host}:5000/')
        os.environ['MLFLOW_S3_ENDPOINT_URL'] = f"http://{minio_host}:9000/" 
        os.environ['AWS_ACCESS_KEY_ID'] = 'minio'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'minio123' 

        print(f"[Kserve] Testing!!", flush=True)
        csv_url = (
            "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
        )   
        data = pd.read_csv(csv_url, sep=";")

        # Split the data into training and test sets. (0.75, 0.25) split.
        train, test = train_test_split(data)

        # The predicted column is "quality" which is a scalar from [3, 9]
        train_x = train.drop(["quality"], axis=1)
        test_x = test.drop(["quality"], axis=1)
        train_y = train[["quality"]]
        test_y = test[["quality"]]

        alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
        l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

        model_url = f"models:/{model_name1}/2"

        model = mlflow.pyfunc.load_model(model_url)
        result = model.predict(test_x)
        print(f"[Result] {result}", flush=True)

        return {"predictions": f"Result : {result}"}


if __name__ == "__main__":
    model = Kserve_model("kserve-test")
    #model.load()
    kserve.ModelServer(workers=1).start([model])