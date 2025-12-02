import joblib
import numpy as np

model = joblib.load("/app/model.joblib") 

def predict(features):
    X = np.array(features).reshape(1, -1)
    return int(model.predict(X)[0])
