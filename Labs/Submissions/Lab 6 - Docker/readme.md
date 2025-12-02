# Iris Flower Classifier - ML Web App

This is a **simple web application** that predicts the species of an Iris flower based on its sepal and petal measurements. It has backend and frontend.

## Features
- Uses a **Random Forest model** trained on the classic Iris dataset.
- Provides a **web interface** to input flower measurements.
- Shows the predicted Iris species: **setosa**, **versicolor**, or **virginica**.
- Fully **Dockerized** — runs in a single container.

## How to Run
1. Build the Docker image:
```bash
docker build -t iris-app .
```

2. Run the container:
```bash
docker run -p 8000:8000 iris-app
```

3. Open the app in your browser:
http://localhost:8000/

4. Enter the measurements and click Predict to see the result.
