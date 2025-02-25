import cv2
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol
import csv
import os

# File path for the CSV file
csv_file = 'qr_code_data.csv'

# Check if the file already exists; if not, create it and write the header
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Identifier', 'Model Number', 'Trimmed Model Number', 'Destination Code', 'Serial Number'])

# Set to store already scanned QR codes
processed_qr_codes = set()

def process_qr_code_image(img):
    processed_qr_codes.clear()
    """Processes the input image and extracts QR code information."""
    # Convert the image to a numpy array
    frame = np.array(img)
    
    # Decode only QR codes from the current frame
    codes = decode(frame, symbols=[ZBarSymbol.QRCODE])

    # Loop through all detected codes
    for code in codes:
        # Decode QR code data
        qr_data = code.data.decode('utf-8').strip()

        # Skip if the QR code has already been processed
        if qr_data in processed_qr_codes:
            continue

        # Add the QR code to the processed set
        processed_qr_codes.add(qr_data)

        print(f"QR Code Detected: {qr_data}")

        # Split the QR code data into fields
        fields = qr_data.split(',')
        if len(fields) >= 5:
            identifier = fields[0].strip()
            model_number = fields[1].strip()
            destination_code = fields[2].strip()
            some_code = fields[3].strip()
            serial_number = fields[4].strip()

            # Trim the model number to the first 7 characters
            trimmed_model_number = model_number[:7]

            # Print extracted data to console
            print(f"Identifier: {identifier}")
            print(f"Model Number: {model_number} (Trimmed: {trimmed_model_number})")
            print(f"Destination Code: {destination_code}")
            print(f"Serial Number: {serial_number}")

            # Save the extracted data into the CSV file
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([identifier, model_number, trimmed_model_number, destination_code, serial_number])
                
        cv2.waitKey(0)
        cv2.destroyAllWindows()