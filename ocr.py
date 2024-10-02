# ocr.py

import cv2
import re
import pytesseract
from PIL import Image
import os

# Set the tesseract_cmd to the location of tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Vvedika\tesseract.exe"

def preprocess_image(image_path):
    """Preprocess the image for better OCR results."""
    # Load the image
    img = cv2.imread(image_path)

    # Resize the image to enhance text visibility
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use adaptive thresholding for binarization
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 11, 2)

    # Morphological operations: closing to fill gaps in text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morph = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)

    # Denoising the image
    denoised = cv2.fastNlMeansDenoising(morph, None, 30, 7, 21)

    # Contrast adjustment (increasing the contrast)
    alpha = 1.5  # Contrast control
    beta = 0     # Brightness control
    adjusted = cv2.convertScaleAbs(denoised, alpha=alpha, beta=beta)

    return adjusted

def filter_kannada_text(text):
    """Filter out unwanted text and keep only Kannada characters and numbers."""
    # Keep only Kannada characters and numbers, remove unwanted words like 'Page'
    filtered_text = re.sub(r'Page\s*\d+', '', text)  # Remove 'Page' followed by any number
    filtered_text = re.sub(r'[^ಅ-ಌಕ-ಹ0-9\s]+', '', filtered_text)  # Keep only Kannada characters and digits
    return filtered_text.strip()  # Remove leading/trailing whitespace

def natural_sort_key(file_name):
    """Generate a sorting key that accounts for numeric values in file names."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', file_name)]

def extract_text_from_images(image_folder, output_txt_file):
    """Perform OCR on images and save the text output."""
    with open(output_txt_file, 'w', encoding='utf-8') as f:
        for image_file in sorted(os.listdir(image_folder), key=natural_sort_key):
            if image_file.endswith('.png'):
                image_path = os.path.join(image_folder, image_file)
                print(f"Processing {image_path}...")

                # Preprocess the image
                processed_img = preprocess_image(image_path)

                # Save the processed image temporarily
                temp_filename = "temp_image.png"
                cv2.imwrite(temp_filename, processed_img)

                # Perform OCR with specified PSM mode
                config = '--psm 6 -l kan'  # PSM for block of text and Kannada language
                text = pytesseract.image_to_string(Image.open(temp_filename), config=config)

                # Filter the extracted text for Kannada and numbers
                filtered_text = filter_kannada_text(text)

                # Only write to the output file if the filtered text is of sufficient length
                if len(filtered_text) >= 10:  # Adjust the minimum length as needed
                    f.write(f"--- Extracted text from {image_file} ---\n")
                    f.write(filtered_text + '\n')
                    f.write("="*50 + '\n')

                print(f"Extracted text from {image_file}")
