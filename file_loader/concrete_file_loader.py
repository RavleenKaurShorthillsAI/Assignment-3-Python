# import pdfplumber
# from docx import Document
# from pptx import Presentation
# from file_loader.abstract_file_loader import FileLoader
 
# class PPTLoader:
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.load_file()
   
 
#     def load_file(self):
#         """Load the PPT file and store its content."""
#         try:
#             self.presentation = Presentation(self.file_path)
#         except Exception as e:
#             print(f"Error loading PPT: {e}")
#             self.presentation = None
 
#     def get_content(self):
#         """Return the content of the PPT file."""
#         return self.presentation
 
#     def close_file(self):
#         """Close the PPT file if necessary."""
#         pass  # Closing not necessary for python-pptx
 

# class DOCXLoader:
#     def __init__(self, file_path):
#         self.file_path = file_path
        
#         self.load_file()

    
 
#     def load_file(self):
#         """Load the DOCX file and store its content."""
#         try:
#             self.document = Document(self.file_path)
#         except Exception as e:
#             print(f"Error loading DOC")
   
#         self.document = None
 
#     def get_content(self):
#         """Return the content of the DOCX file."""
#         return self.document
 
#     def close_file(self):
#         """Close the DOCX file if necessary."""
#         pass  # Closing not necessary for python-docx
# class PDFLoader:
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.load_pdf()  # Load the PDF immediately during initialization

 
#     def load_pdf(self):
#         """Load the PDF file and store its content."""
#         try:
#             self.pdf = pdfplumber.open(self.file_path)
#             self.content = self.pdf.pages  # Store all pages
#         except Exception as e:
#             print(f"Error loading PDF: {e}")
#             self.content = None
 
#     def load_file(self):
#         """Return the loaded content (in this case, the pages of the PDF)."""
#         return self.content
 
#     def close_pdf(self):
#         """Close the PDF file."""
#         if self.pdf:
#             self.pdf.close()
 
 
import pdfplumber
from docx import Document
from pptx import Presentation
from abc import ABC, abstractmethod
import os

# Abstract class FileLoader
class FileLoader(ABC):
    def __init__(self, file_path, file_type):
        self.file_path = file_path
        self.file_type = file_type # Extracts the file extension
        self.file = None

    @abstractmethod
    def load_file(self):
        """Abstract method to load the file based on the file type."""
        pass

    def validate_file(self):
        """Validate that the file exists and its type is supported."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File does not exist: {self.file_path}")
        if self.file_type not in ['pdf', 'docx', 'pptx']:
            raise ValueError(f"Unsupported file type: {self.file_type}. Only PDF, DOCX, and PPTX are supported.")

# Concrete Loader class that handles loading of files
class Loader(FileLoader):

    file_reader = {
        'pdf': pdfplumber.open,
        'docx': Document,
        'pptx': Presentation,
    }

    def load_file(self):
        """Load the file based on the file type."""
        self.validate_file()  # First validate the file

        try:
            self.file = self.file_reader[self.file_type](self.file_path)
        except Exception as e:
            raise ValueError(f"Error loading file: {e}")

 
