# Lab 1 - Streamlit + FastAPI

This project demonstrates a simple **Iris Flower Prediction** app using **FastAPI** as backend and **Streamlit** as frontend.

---

## Running the FastAPI backend

1. Open a terminal and navigate to the FastAPI `src` folder:

    cd "Lab 1 - Streamlit+FastApi/FastAPI/src"

2. Run the FastAPI app using uvicorn:

    uvicorn main:app --reload

    FastAPI server will run at:

    http://127.0.0.1:8000

    You can check the  swagger documnentation at http://127.0.0.1:8000/docs

## Running the Streamlit dashboard

1. Open a new terminal and navigate to the Streamlit src folder:

    cd "Lab 1 - Streamlit+FastApi/Streamlit/src"

2. Run the Dashboard:

    streamlit run Dashboard.py

    Streamlit will automatically open in your default browser.

3. Upload a JSON test file or use the Random Sample button to test predictions.

    Make sure the FastAPI server is running before using the dashboard.