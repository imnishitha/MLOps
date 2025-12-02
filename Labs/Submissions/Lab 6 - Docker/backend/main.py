from fastapi import FastAPI
from pydantic import BaseModel
from backend.model import predict
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

CLASS_NAMES = ["setosa", "versicolor", "virginica"]

@app.post("/predict")
def get_prediction(data: IrisInput):
    features = [
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width,
    ]
    pred_index = predict(features)
    pred_name = CLASS_NAMES[pred_index]  # map number to name
    return {"class": pred_name}
