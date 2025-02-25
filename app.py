import streamlit as st
import cv2
import numpy as np
import pandas as pd
import time
import json
from datetime import datetime
from PIL import Image
from streamlit_cropper import st_cropper
from qr_reader import process_qr_code_image
from reader_app import extract_text_from_image

ROI_FILE = "roi_profiles.json"
QR_CODE_DATA_FILE = "qr_code_data.csv"  

# Load or initialize ROI profiles
def load_roi_profiles():
    try:
        with open(ROI_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_roi_profiles(profiles):
    with open(ROI_FILE, "w") as file:
        json.dump(profiles, file, indent=4)

def get_latest_trimmed_model_number():
    try:
        # Load the CSV file containing the QR code details
        df = pd.read_csv(QR_CODE_DATA_FILE)
        # Assuming the column is named 'Trimmed Model Number', adjust if needed
        latest_trimmed_model_number = df['Trimmed Model Number'].iloc[-1]
        return latest_trimmed_model_number
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return None

# Streamlit Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Custom Cropping Profile", "Carton Box Inspection System"])

if page == "Custom Cropping Profile":
    st.title("Custom Cropping Profile")
    profiles = load_roi_profiles()

    if "camera" not in st.session_state:
        st.session_state.camera = None

    if st.button("Start Camera"):
        if st.session_state.camera is None or not st.session_state.camera.isOpened():
            st.session_state.camera = cv2.VideoCapture(0)

    FRAME_WINDOW = st.empty()
    if st.session_state.camera and st.session_state.camera.isOpened():
        ret, frame = st.session_state.camera.read()
        if ret:
            FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption="Live Camera Feed")

    if st.button("Capture"):
        if st.session_state.camera and st.session_state.camera.isOpened():
            ret, frame = st.session_state.camera.read()
            if ret:
                st.session_state.captured_frame = frame
                st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption="Captured Image")

    if "captured_frame" in st.session_state:
        img = Image.fromarray(cv2.cvtColor(st.session_state.captured_frame, cv2.COLOR_BGR2RGB))
        rect = st_cropper(img, box_color="#0000FF", return_type="box")
        left, top, width, height = tuple(map(int, rect.values()))
        cropped_img = img.crop((left, top, left + width, top + height))
        st.image(cropped_img, caption="Cropped Preview")
        
        model_name = st.text_input("Enter Model Name:")
        if st.button("Save ROI") and model_name:
            profiles[model_name] = [left, top, width, height]
            save_roi_profiles(profiles)
            st.success(f"ROI saved for model: {model_name}")

elif page == "Carton Box Inspection System":
    st.title("Carton Box Inspection System")
    profiles = load_roi_profiles()
    model_name = st.selectbox("Select Model", options=list(profiles.keys()))
    
    placeholder_cam0 = st.empty()
    placeholder_cam1 = st.empty()
    
    def initialize_camera(cam_index):
        cap = cv2.VideoCapture(cam_index)
        if not cap.isOpened():
            st.warning(f"Camera {cam_index} not found.")
            return None
        return cap
    
    cap0 = initialize_camera(1)
    cap1 = initialize_camera(0)

    if cap0 and cap1:
        st.success("Both cameras initialized. Streaming...")

        # Auto-capture frames every 10 seconds
        last_capture_time = time.time()
        capture_interval = 10  # Capture every 10 seconds

        while True:
            current_time = time.time()
            if current_time - last_capture_time >= capture_interval:
                last_capture_time = current_time

                # Camera 0: QR Code
                ret0, frame0 = cap0.read()
                if ret0:
                    frame0_rgb = cv2.cvtColor(frame0, cv2.COLOR_BGR2RGB)
                    placeholder_cam0.image(frame0_rgb, caption="QR Code Camera")
                    filename0 = f"qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    cv2.imwrite(filename0, cv2.cvtColor(frame0, cv2.COLOR_RGB2BGR))
                    qr_text = process_qr_code_image(Image.open(filename0))

                    # st.write("QR Text Extracted: ", qr_text)  

                # Camera 1: OCR
                ret1, frame1 = cap1.read()
                if ret1:
                    frame1_rgb = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
                    placeholder_cam1.image(frame1_rgb, caption="OCR Camera")
                    filename1 = f"ocr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    cv2.imwrite(filename1, cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR))

                    roi = profiles.get(model_name, [0, 0, 100, 100])
                    x, y, w, h = roi
                    image_pil = Image.open(filename1)
                    cropped_img = image_pil.crop((x, y, x + w, y + h))
                    st.image(cropped_img, caption="Cropped Image for OCR")
                    extracted_text = extract_text_from_image(cropped_img)

                    # st.write("Extracted Text: ", extracted_text)  

                    # Compare the latest trimmed model number with the extracted text
                    latest_trimmed_model_number = get_latest_trimmed_model_number()
                    if latest_trimmed_model_number and extracted_text and extracted_text.strip().lower() == latest_trimmed_model_number.strip().lower():
                        st.success("PASS")
                    else:
                        st.error("FAIL")
                  
    if cap0:
        cap0.release()
    if cap1:
        cap1.release()