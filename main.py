import os
from Data_Cleaning import KannadaDataCleaner  # Import your cleaner class
from ocr import extract_text_from_images

def search_keywords(text_corpus, keyword):
    """Search for keywords or phrases in the extracted text corpus."""
    results = []
    for idx, text in enumerate(text_corpus):
        if keyword in text:
            results.append((idx, text))  # Store index and text if keyword is found
    return results

def main():
    # Specify the paths
    image_folder = "path_to_your_images"  # Update this path to your images
    cleaned_output_file = "cleaned_data.txt"  # Output file for cleaned data
    extracted_output_file = "extracted_text.txt"  # Intermediate file for extracted text

    # Extract text from images
    extracted_texts = extract_text_from_images(image_folder)

    # Save extracted data to a text file (if necessary)
    with open(extracted_output_file, 'w', encoding='utf-8') as f:
        for text in extracted_texts:
            f.write(text + '\n')

    # Initialize the cleaner and clean the extracted text
    cleaner = KannadaDataCleaner()
    cleaner.process_raw_data(extracted_texts)

    # Save cleaned data to file
    cleaner.save_to_file(cleaned_output_file)

    # Keyword search
    keyword = input("Enter a keyword or phrase to search: ")
    cleaned_texts = cleaner.get_cleaned_data()  # Get cleaned data
    search_results = search_keywords(cleaned_texts, keyword)

    if search_results:
        print(f"Found {len(search_results)} occurrences of '{keyword}':")
        for idx, text in search_results:
            print(f"Document {idx}: {text}")
    else:
        print(f"No occurrences of '{keyword}' found.")

if __name__ == "__main__":
    main()
