import json
import requests
import streamlit as st
from pathlib import Path
from streamlit.logger import get_logger

# If you start the fast api server on a different port
# make sure to change the port below
FASTAPI_BACKEND_ENDPOINT = "http://localhost:8000"

# Make sure you have iris_model.pkl file in FastAPI_Labs/src folder.
# If it's missing run train.py in FastAPI_Labs/src folder
# If your FastAPI_Labs folder name is different, update accordingly in the following path
FASTAPI_IRIS_MODEL_LOCATION = Path(__file__).resolve().parents[2] / 'FastAPI_Labs' / 'model' / 'iris_model.pkl'

# streamlit logger
LOGGER = get_logger(__name__)

def run():
    # Set the main dashboard page browser tab title and icon
    st.set_page_config(
        page_title="Iris Flower Prediction Demo",
        page_icon="🪻",
    )

    # Header
    st.title("🌸 Iris Flower Prediction Dashboard")
    st.markdown("Upload your input file or use a random sample to get predictions powered by FastAPI + Streamlit.")

    # Sidebar: backend health check
    with st.sidebar:
        st.header("⚙️ Configuration")
        try:
            # Make sure fast api is running. Check the lab for guidance on getting
            # the server up and running
            backend_request = requests.get(FASTAPI_BACKEND_ENDPOINT)
            # If backend returns successful connection (status code: 200)
            if backend_request.status_code == 200:
                # This creates a green box with message
                st.success("Backend online ✅")
            else:
                # This creates a yellow bow with message
                st.warning("Problem connecting 😭")
        except requests.ConnectionError as ce:
            LOGGER.error(ce)
            st.error("❌ Backend offline")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.subheader("📂 Input Options")
        if st.button("🎲 Use Random Sample"):
            try:
                response = requests.get(f"{FASTAPI_BACKEND_ENDPOINT}/random_sample")
                if response.status_code == 200:
                    random_sample = response.json()
                    st.session_state["RANDOM_SAMPLE"] = random_sample
                    st.session_state["IS_JSON_FILE_AVAILABLE"] = True
                    st.success("🎉 Random sample loaded!")
                else:
                    st.error(f"Failed to fetch random sample: {response.status_code}")
            except Exception as e:
                LOGGER.error(e)
                st.error("Error connecting to backend for random sample.")

        test_input_file = st.file_uploader(
            "Or upload your own JSON file",
            type=['json'],
            label_visibility="collapsed",
            help="Upload a JSON file with the input_test field."
        )


    if test_input_file:
        test_input_data = json.load(test_input_file)
        st.write("### 🔎 File Preview")
        st.json(test_input_data)
        st.session_state["IS_JSON_FILE_AVAILABLE"] = True
    elif "RANDOM_SAMPLE" in st.session_state:
        test_input_data = st.session_state["RANDOM_SAMPLE"]
        st.write("### 🔎 Random Sample Preview")
        st.json(test_input_data)
    else:
        st.session_state["IS_JSON_FILE_AVAILABLE"] = False
        test_input_data = None

    # Centered predict button
    with col2:
        predict_button = st.button("🚀 Predict", use_container_width=True)

    # Prediction results
    st.divider()
    st.subheader("📊 Prediction Results")

    # Dashboard body
    # Heading for the dashboard
    st.write("# Iris Flower Prediction! 🪻")
    # If predict button is pressed
    if predict_button:
        if st.session_state.get("IS_JSON_FILE_AVAILABLE", False) and test_input_data:
            if FASTAPI_IRIS_MODEL_LOCATION.is_file():
                # The input needs to be converted from dictionary
                # to JSON since content exchange format type is set
                # as JSON by default
                # client_input = json.dumps({
                #     "petal_length": petal_length,
                #     "sepal_length": sepal_length,
                #     "petal_width": petal_width,
                #     "sepal_width": sepal_width
                # })
                client_input = json.dumps(test_input_data['input_test'])
                try:
                    # This holds the result. Acts like a placeholder
                    # that we can fill and empty as required
                    result_container = st.empty()
                    # While the model predicts show a spinner indicating model is
                    # running the prediction
                    with st.spinner('Predicting...'):
                        # Send post request to backend predict endpoint
                        predict_iris_response = requests.post(f'{FASTAPI_BACKEND_ENDPOINT}/predict', client_input)
                    # If prediction status OK
                    if predict_iris_response.status_code == 200:
                        # Convert response from JSON to dictionary
                        iris_content = json.loads(predict_iris_response.content)
                        start_sentence = "The flower predicted is: "
                        if iris_content["response"] == 0:
                            result_container.success(f"{start_sentence} setosa")
                        elif iris_content["response"] == 1:
                            result_container.success(f"{start_sentence} versicolor")
                        elif iris_content["response"] == 2:
                            result_container.success(f"{start_sentence} virginica")
                        else:
                            result_container.error("Some problem occured while prediction")
                            LOGGER.error("Problem during prediction")
                    else:
                        # Pop up notification at bottom-left if backend is down
                        st.toast(f':red[Status from server: {predict_iris_response.status_code}. Refresh page and check backend status]', icon="🔴")
                except Exception as e:
                    # Pop up notification if backend is down
                    st.toast(':red[Problem with backend. Refresh page and check backend status]', icon="🔴")
                    LOGGER.error(e)
            else:
                # Message for iris_model.pkl not found
                LOGGER.warning('iris_model.pkl not found in FastAPI Lab. Make sure to run train.py to get the model.')
                st.toast(':red[Model iris_model.pkl not found. Please run the train.py file in FastAPI Lab]', icon="🔥")
        else:
            st.error("Please upload a JSON file or use the random sample button first.")

if __name__ == "__main__":
    run()