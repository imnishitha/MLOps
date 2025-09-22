import json
import requests
import streamlit as st
from pathlib import Path
from streamlit.logger import get_logger

# FastAPI backend endpoint
FASTAPI_BACKEND_ENDPOINT = "http://localhost:8000"
FASTAPI_IRIS_MODEL_LOCATION = Path(__file__).resolve().parents[2] / 'FastAPI_Labs' / 'model' / 'iris_model.pkl'

# Streamlit logger
LOGGER = get_logger(__name__)

def run():
    # Page settings
    st.set_page_config(
        page_title="🌸 Iris Flower Prediction",
        page_icon="🪻",
        layout="wide"
    )

    # Header
    st.title("🌸 Iris Flower Prediction Dashboard")
    st.markdown("Upload your input file and get instant predictions powered by FastAPI + Streamlit.")

    # Sidebar: backend health check
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Backend health check
        try:
            backend_request = requests.get(FASTAPI_BACKEND_ENDPOINT)
            if backend_request.status_code == 200:
                st.success("✅ Backend online")
            else:
                st.warning("⚠️ Backend reachable but not healthy")
        except requests.ConnectionError as ce:
            LOGGER.error(ce)
            st.error("❌ Backend offline")

    # Centered file uploader
    st.subheader("📂 Upload test prediction JSON file")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        test_input_file = st.file_uploader(
            "Choose a file",
            type=['json'],
            label_visibility="collapsed",
            help="Upload a JSON file with the input_test field."
        )

    if test_input_file:
        st.write("### 🔎 File Preview")
        test_input_data = json.load(test_input_file)
        st.json(test_input_data)
        st.session_state["IS_JSON_FILE_AVAILABLE"] = True
    else:
        st.session_state["IS_JSON_FILE_AVAILABLE"] = False

    # Centered predict button
    with col2:
        predict_button = st.button("🚀 Predict", use_container_width=True)

    # Prediction results
    st.divider()
    st.subheader("📊 Prediction Results")

    if predict_button:
        if st.session_state.get("IS_JSON_FILE_AVAILABLE", False):
            if FASTAPI_IRIS_MODEL_LOCATION.is_file():
                client_input = json.dumps(test_input_data['input_test'])
                try:
                    result_container = st.empty()
                    with st.spinner("🔮 Model is predicting..."):
                        predict_iris_response = requests.post(
                            f"{FASTAPI_BACKEND_ENDPOINT}/predict", client_input
                        )
                    if predict_iris_response.status_code == 200:
                        iris_content = json.loads(predict_iris_response.content)
                        label_map = {0: "Setosa 🌱", 1: "Versicolor 🌿", 2: "Virginica 🌸"}
                        predicted_label = label_map.get(iris_content["response"], "Unknown ❓")
                        result_container.success(f"✅ The flower predicted is: **{predicted_label}**")
                    else:
                        st.toast(
                            f":red[Server returned {predict_iris_response.status_code}. Try again.]",
                            icon="🔴"
                        )
                except Exception as e:
                    st.toast(":red[Problem with backend connection.]", icon="🔴")
                    LOGGER.error(e)
            else:
                LOGGER.warning("iris_model.pkl not found")
                st.toast(":red[Model not found. Please run train.py to generate iris_model.pkl]", icon="🔥")
        else:
            LOGGER.error("No valid JSON file provided")
            st.toast(":red[Please upload a valid JSON file with input_test field.]", icon="⚠️")

if __name__ == "__main__":
    run()
