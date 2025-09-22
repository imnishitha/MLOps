import random
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from predict import predict_data

app = FastAPI()


class IrisData(BaseModel):
    petal_length: float
    sepal_length: float
    petal_width: float
    sepal_width: float

class IrisResponse(BaseModel):
    response: int

class IrisSampleResponse(BaseModel):
    input_test: IrisData

@app.get("/", status_code=status.HTTP_200_OK)
async def health_ping():
    return {"status": "healthy"}

@app.post("/predict", response_model=IrisResponse)
async def predict_iris(iris_features: IrisData):
    try:
        features = [[iris_features.sepal_length, iris_features.sepal_width,
                     iris_features.petal_length, iris_features.petal_width]]
        prediction = predict_data(features)
        return IrisResponse(response=int(prediction[0]))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/random_sample", response_model=IrisSampleResponse)
async def random_iris_sample():
    """
    Returns a random iris flower sample with realistic feature ranges.
    """
    sample = IrisData(
        sepal_length=round(random.uniform(4.3, 7.9), 1),
        sepal_width=round(random.uniform(2.0, 4.4), 1),
        petal_length=round(random.uniform(1.0, 6.9), 1),
        petal_width=round(random.uniform(0.1, 2.5), 1)
    )
    return IrisSampleResponse(input_test=sample)
