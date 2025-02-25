# **Carton Box Inspection System**  

The **Carton Box Inspection System** is a **computer vision-based quality control solution** that automates the validation of carton box model numbers using **Streamlit**, **OpenCV**, **Tesseract OCR**, and **pyzbar** for QR code processing. It uses **dual USB cameras** one for **QR code scanning** and another for **OCR-based text extraction** to compare the extracted model number against the QR code data, ensuring accurate inspection.  

## **📌 Features**  

✅ **Dual Camera Support** – Uses two USB cameras:  
&nbsp;&nbsp;&nbsp;&nbsp;📷 *Camera 1:* Scans QR codes.  
&nbsp;&nbsp;&nbsp;&nbsp;📷 *Camera 2:* Captures text for OCR-based model number extraction.  

✅ **QR Code Processing** – Reads and decodes QR codes from images in real-time.  

✅ **OCR-Based Model Number Extraction** – Extracts model numbers from a pre-defined region in the image.  

✅ **Custom Cropping Profiles** – Allows users to define, save, and reuse cropping regions for different models.  

✅ **Automated Quality Control** – Compares the extracted text with the QR model number and determines a **Pass/Fail** status.  

✅ **Real-time Processing** – Captures images every 10 seconds, processes them, and updates inspection results dynamically.  

## **🛠️ Installation**  

### **🔹 Step 1: Clone the Repository**  
```bash
git clone https://github.com/your-repo/carton-box-inspection.git  
cd carton-box-inspection  
```

### **🔹 Step 2: Install Dependencies**  
Ensure you have **Python 3.8+** installed, then run:  
```bash
pip install -r requirements.txt  
```

### **🔹 Step 3: Run the Application**  
```bash
streamlit run app.py  
```

---

## **💾 Hardware Requirements**  

🔹 **Two USB cameras** – Required for QR scanning and OCR-based text recognition.  
🔹 **Computer with Python 3.8+** – To run the Streamlit application and process images.  
🔹 **Tesseract OCR Installed** – Ensure `pytesseract` can access `tesseract-ocr`.  

📌 *[Download Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and add it to your system PATH.*  

## **🚀 Usage Guide**  

### **1️⃣ Custom Cropping Profile Setup**  
1. Open the **Custom Cropping Profile** page in the Streamlit app.  
2. Capture an image using the **OCR Camera**.  
3. Select a **Region of Interest (ROI)** for model number extraction.  
4. Save the cropping profile with a **unique model name**.  

### **2️⃣ Running the Inspection System**  
1. Select a **model name** from the saved profiles.  
2. The system captures images from both cameras every **10 seconds**.  
3. It extracts data from the **QR code** and **OCR result**.  
4. If the extracted model number matches the QR code model number, it displays ✅ **PASS**; otherwise, ❌ **FAIL**.  

## **📂 Project Structure**  
```
📂 carton-box-inspection  
│── app.py              # Main Streamlit app  
│── qr_reader.py        # QR Code processing script  
│── reader_app.py       # OCR extraction script  
│── requirements.txt    # List of dependencies  
│── roi_profiles.json   # Saved cropping profiles  
│── qr_code_data.csv    # Stored QR code data  
│── README.md           # Project documentation  
```

## **📜 requirements.txt**  

Ensure all required dependencies are installed by running `pip install -r requirements.txt`:  
```
streamlit
opencv-python
pytesseract
pyzbar
numpy
pandas
Pillow
```

## **💡 Contributing**  
🔹 Fork the repository.  
🔹 Create a new branch (`git checkout -b feature-name`).  
🔹 Commit your changes (`git commit -m "Added new feature"`).  
🔹 Push the branch (`git push origin feature-name`).  
🔹 Open a Pull Request.  

## **📝 License**  
This project is licensed under the **MIT License** – feel free to modify and use it!  
