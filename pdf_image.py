# pdf_to_images.py

import fitz  # PyMuPDF
import os

def pdf_to_images(pdf_path, output_folder='output_images/', dpi=300):
    """Convert PDF pages to images using PyMuPDF."""
    # List contents of the current directory for debugging
    print("Current directory contents before creating output folder:")
    print(os.listdir(os.getcwd()))
    
    # Create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
    else:
        print(f"Output folder already exists: {output_folder}")
    
    # Check if PDF file exists
    pdf_exists = os.path.exists(pdf_path)
    print(f"Checking if PDF file exists: {pdf_exists} at {pdf_path}")

    if not pdf_exists:
        print("PDF file does not exist. Please check the path.")
        return []
    
    images_paths = []  # List to store the paths of saved images

    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)
        print(f"Converting {pdf_path} to images...")
        
        # Iterate through each page in the PDF
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)  # Load the page
            pix = page.get_pixmap(dpi=dpi)  # Render page to image
            output_image_path = f"{output_folder}page_{page_num + 1}.png"
            pix.save(output_image_path)  # Save the image
            images_paths.append(output_image_path)  # Store the path of the saved image
            print(f"Saved image: {output_image_path}")
        
        print(f"Successfully saved {len(doc)} images to {output_folder}.")
        return images_paths  # Return the list of image paths

    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        print(f"Check if output folder is writable: {os.access(output_folder, os.W_OK)}")
