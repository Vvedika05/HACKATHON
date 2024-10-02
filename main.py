import os
from pdf_image import pdf_to_images
from ocr import extract_text_from_images
from Data_Cleaning import KannadaDataCleaner

def search_in_cleaned_data(search_term, cleaned_txt_file):
    """
    Search for a keyword or phrase in the cleaned text file and print the results
    with the corresponding page number and line number.
    """
    found = False
    current_page = 1  # Start on page 1
    line_count = 0    # Initialize line count for current page
    
    with open(cleaned_txt_file, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, start=1):
            if line.strip() == "":  # Assuming a blank line indicates a page break
                current_page += 1
                line_count = 0  # Reset line count for new page
                continue
            
            line_count += 1  # Increment line count
            
            if search_term.lower() in line.lower():  # Case-insensitive search
                print(f"Found on page {current_page}, line {line_count}: {line.strip()}")
                found = True
    
    if not found:
        print(f"No results found for '{search_term}'.")


def main():
    pdf_path = input("Enter the path to the PDF file: ")
    output_folder = 'output_images/'  # Folder where images will be saved
    output_txt_file = 'extracted_text.txt'  # File to save extracted text
    cleaned_txt_file = 'cleaned_text.txt'  # File to save cleaned text

    # Step 1: Convert PDF to images
    print("Step 1: Converting PDF to images...")
    images_paths = pdf_to_images(pdf_path, output_folder)

    if not images_paths:  # Check if any images were created
        print("No images were created. Exiting.")
        return

    # Step 2: Extract text from images
    print("Step 2: Extracting text from images...")
    extract_text_from_images(output_folder, output_txt_file)
    
    # Step 3: Clean the extracted data
    print("Step 3: Cleaning the extracted data...")
    cleaner = KannadaDataCleaner()

    # Read the extracted text from the output file
    with open(output_txt_file, 'r', encoding='utf-8') as f:
        raw_data = f.readlines()
    
    # Process and clean the raw data
    cleaner.process_raw_data(raw_data)
    cleaned_data = cleaner.get_cleaned_data()

    # Join the cleaned data into a single string
    cleaned_data_str = "\n".join(cleaned_data)  # Join list into a single string

    # Write cleaned data to a new file
    with open(cleaned_txt_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_data_str)

    print(f"Cleaned text saved to {cleaned_txt_file}.")

     # Step 4: Search for a keyword or phrase
    search_term = input("Enter a keyword or phrase to search in the cleaned text: ")
    search_in_cleaned_data(search_term, cleaned_txt_file)

if __name__ == '__main__':
    main()




   


