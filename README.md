# PDF, DOCX, and PPTX Data Extractor
This project provides a modular Python solution to extract text, hyperlinks, images, and tables from PDF, DOCX, and PPTX files while capturing metadata such as file type, page/slide numbers, font styles, and more. The project also includes functionality to store the extracted data in both files and a MySQL database.
## Project Structure
```
Python-Assignment/
│
│   ├── file_loader/
│   │   ├── __init__.py
│   │   ├── file_loader.py  # Abstract file loader class
│   │   ├── pdf_loader.py   # Concrete class for handling PDFs
│   │   ├── docx_loader.py  # Concrete class for handling DOCX files
│   │   ├── ppt_loader.py   # Concrete class for handling PPT files
│   │
│   ├── data_extractor/
│   │   ├── __init__.py
│   │   ├── data_extractor.py  # Class for extracting text, images, links, tables from files
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── file_storage.py  # Concrete class for storing data in files
│   │   ├── sql_storage.py   # Concrete class for storing data in an SQL database
│
├── tests/
│   ├── __init__.py
├── requirements.txt   # Dependencies like PyMuPDF, python-docx, python-pptx, mysql-connector-python, etc.
├── README.md          # Overview of the project and instructions
└── testing.py         # Main script to run all the tests

```
## Features
- Text Extraction: Extracts plain text from PDF, DOCX, and PPTX files along with metadata (font style, page number, slide number, headings).
- Hyperlink Extraction: Extracts URLs and linked text from PDF, DOCX, and PPTX files.
- Image Extraction: Extracts images and metadata (resolution, format, page/slide number) and stores them in separate folders.
- Table Extraction: Extracts tables and stores them in CSV format for each file type.
- Storage Options:
  - File Storage: Saves text, links, images, and tables into separate files.
  - SQL Storage: Stores extracted data into a MySQL database.
## Installation
- Clone the repo:
```
git clone https://github.com/your_username/pdf-docx-pptx-extractor.git
cd pdf-docx-pptx-extractor
```
- Set up a Python virtual environment and install dependencies:
```
python -m venv env
source env/bin/activate   # On Windows use `env\Scripts\activate`
pip install -r requirements.txt
```
- Set up your MySQL database and create a .env file for MySQL credentials:
```
DB_HOST=your_host
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database
```
## Usage
- Run the main script:
```
python main.py
```
- The extracted data will be saved in the output/ folder and organized into subfolders based on file type (PDF, DOCX, PPTX). Additionally, data will be stored in the MySQL database if configured correctly.
## Manual Testing
Test cases have been manually prepared and provided in the Excel file and can be tested with different file types and scenarios:
- PDF: Small, large, corrupted PDFs.
- DOCX: Small, large, corrupted DOCX files.
- PPTX: Small, large, corrupted PPTX files.
Please refer to the `test_files/` folder for these files.
## Unit Testing
Unit tests are planned to cover the following aspects:
- File validation and loading
- Text extraction
- Hyperlink extraction
- Image Extraction
- Table extraction
- MySQL data storage
To run unit tests:
```
pytest tests/test_extractor.py
```
