import streamlit as st
import cv2
import pytesseract
import numpy as np
from PIL import Image

# Function to read the image and extract text using OCR
def extract_text_from_image(image):
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Resize the image if it's too small (optional, adjust as needed)
    # if img.shape[0] < 500 or img.shape[1] < 500:
    #     img = cv2.resize(img, (1000, 1000))  # Resize to 1000x1000 (or another appropriate size)
    #     print(f"Resized image size: {img.shape}")  # Print resized image size

    # Pre-process the image for better OCR results
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Extract text from the processed image using Tesseract OCR
    ocr_result = pytesseract.image_to_string(thresh, config='--psm 6')
    extracted_text = ocr_result.strip().replace('\n', '').replace(' ', '')

    # Print the extracted text in the CMD/Console
    print(f"Extracted Text: {extracted_text}")

    return extracted_text

# Reader page function
def reader_page():
    st.title("OCR Reader")

    if "cropped_image" in st.session_state:
        cropped_image = st.session_state.cropped_image

        # Check if the cropped image is empty
        if cropped_image.size == 0:
            st.error("The cropped image is empty. Please check the cropping coordinates.")
        else:
            # Display the cropped image
            st.image(cropped_image, caption="Cropped Image", use_container_width=True)
            st.write("Processing...")

            # Perform OCR on the cropped image
            extracted_text = extract_text_from_image(cropped_image)

            if extracted_text:
                st.success("Extracted Text:")
                st.write(extracted_text)
            else:
                st.error("Failed to extract text from the image.")
    else:
        st.error("No cropped image found. Please go back to the Cropper page.")