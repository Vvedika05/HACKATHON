#Data Cleaning

import re

class KannadaDataCleaner:
    def __init__(self):
        self.cleaned_data = []  # Store cleaned data for all pages
        self.current_page = []  # Store content for the current page
        self.page_number = 1  # Initialize page number

    def clean_text(self, text):
        """Clean the extracted text while retaining duplicates and format."""
        # Keep only Kannada characters and numbers
        cleaned = re.sub(r'[^ಅ-ಌಕ-ಹ0-9\s]+', '', text)  
        cleaned = cleaned.strip()  # Remove leading/trailing whitespace
        
        # Normalize spaces
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Replace multiple spaces with a single space
        
        # Remove excessive repetitive characters
        cleaned = self.remove_repetitive_characters(cleaned)

        # Remove lines with excessive repetitive characters
        if cleaned and self.is_meaningful(cleaned):
            return cleaned
        return None

    def remove_repetitive_characters(self, text):
        """Remove excessive consecutive characters, keeping only the last occurrence."""
        # Use regular expression to replace consecutive duplicates with a single character
        return re.sub(r'(.)\1+', r'\1', text)

    def is_meaningful(self, text):
        """Check if the text is meaningful (not just a single repeating character)."""
        if len(text) > 3:
            return len(set(text)) > 1  # Check for multiple unique characters
        return True  # Short lines are meaningful if they are not repetitive

    def process_raw_data(self, raw_data):
        """Process the raw data into cleaned lines while retaining formatting."""
        for line in raw_data:
            # Check for page break markers
            if "==================================================" in line or "--- Extracted text from" in line:
                if self.current_page:  # If there's content to save
                    # Add page number before the current page content
                    page_content = f"Page {self.page_number}\n" + "\n".join(self.current_page) + "\n\n--- End of Page ---\n\n"
                    self.cleaned_data.append(page_content)
                    self.current_page = []  # Reset for the next page
                    self.page_number += 1  # Increment page number
                continue  # Skip processing this line

            # Process the line if it's not a page break marker
            cleaned_line = self.clean_text(line)
            if cleaned_line:  # Only process if the line is meaningful
                self.current_page.append(cleaned_line)  # Store cleaned line

        # After processing all lines, add the remaining current page content if any
        if self.current_page:
            # Add page number before the last page content
            page_content = f"Page {self.page_number}\n" + "\n".join(self.current_page) + "\n\n--- End of Page ---\n\n"
            self.cleaned_data.append(page_content)

    def get_cleaned_data(self):
        """Return the cleaned data."""
        return self.cleaned_data

    def save_to_file(self, output_file):
        """Save cleaned data to a text file."""
        with open(output_file, 'w', encoding='utf-8') as file:
            for page in self.cleaned_data:
                file.write(f"{page}")
        print(f"Cleaned data saved to {output_file}")

# Example of how to use this in practice
if __name__ == "__main__":
    def load_data(file_path):
        """Load data from a text file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.readlines()

    input_file = 'extracted_text.txt'
    output_file = 'cleaned_data.txt'
    
    raw_data = load_data(input_file)

    cleaner = KannadaDataCleaner()

    cleaner.process_raw_data(raw_data)

    cleaner.save_to_file(output_file)
