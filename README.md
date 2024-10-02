# HACKATHON
# Handwritten Document Keyword Search Model

## Overview
The Handwritten Document Keyword Search Model is designed to convert PDF documents into images, extract text from these images using Optical Character Recognition (OCR), and clean the extracted text. The model allows users to efficiently search for specific keywords or phrases within the cleaned data, making it especially useful for researchers needing to locate specific information in large datasets of handwritten documents without the need for digitization.

## Features
- **PDF to Image Conversion**: Convert PDF files into images for OCR processing.
- **Text Extraction**: Extract text from images using OCR technologies.
- **Data Cleaning**: Clean the extracted text for improved readability and structure.
- **Keyword Search**: Search for specific keywords or phrases, returning the page number and line number for each occurrence found.

## Technologies Used
- **Python**: The programming language used for development.
- **OCR Library**: (e.g., Tesseract) for text extraction from images.
- **PDF to Image Library**: (e.g., pdf2image) for converting PDF files to images.
- **Custom Data Cleaning Module**: `Data_Cleaning` for processing and cleaning text data.
- **Optional**: Kannada Data Cleaning features (if applicable).

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your_username/handwritten_keyword_search.git
   cd handwritten_keyword_search
