import pdfplumber
from docx import Document
from pptx import Presentation
from abc import ABC, abstractmethod
import os

# Abstract class FileLoader
class FileLoader(ABC):
    """
    Abstract base class for file loaders. 
    Defines a standard interface for loading different types of files (PDF, DOCX, PPTX).
    """
    def __init__(self, file_path, file_type):
        """
        Initialize the FileLoader with the file path and file type.
        :param file_path: The path of the file to be loaded.
        :param file_type: The type of the file (extension like 'pdf', 'docx', 'pptx').
        """
        self.file_path = file_path
        self.file_type = file_type  # Extracts and stores the file extension
        self.file = None  # Placeholder for the file object once it's loaded

    @abstractmethod
    def load_file(self):
        """
        Abstract method to load the file based on the file type.
        Each concrete class must implement this method.
        """
        pass

    def validate_file(self):
        """
        Validate that the file exists and its type is supported.
        :raises FileNotFoundError: If the file doesn't exist.
        :raises ValueError: If the file type is not supported.
        """
        # Check if the file exists at the given file path
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File does not exist: {self.file_path}")
        
        # Ensure the file type is one of the supported types
        if self.file_type not in ['pdf', 'docx', 'pptx']:
            raise ValueError(f"Unsupported file type: {self.file_type}. Only PDF, DOCX, and PPTX are supported.")

# Concrete Loader class that handles loading of files
class Loader(FileLoader):
    """
    Concrete implementation of the FileLoader class.
    Handles loading of files based on their type (PDF, DOCX, PPTX).
    """

    # A dictionary mapping file types to the appropriate library functions to open the file
    file_reader = {
        'pdf': pdfplumber.open,  # Use pdfplumber to open PDF files
        'docx': Document,        # Use python-docx to open DOCX files
        'pptx': Presentation,    # Use python-pptx to open PPTX files
    }

    def load_file(self):
        """
        Load the file based on its type after validating it.
        :raises ValueError: If there is an issue loading the file.
        """
        # First, validate the file for existence and supported type
        self.validate_file()

        try:
            # Use the appropriate file reader based on the file type to load the file
            self.file = self.file_reader[self.file_type](self.file_path)
        except Exception as e:
            # If something goes wrong during file loading, raise a ValueError with the error details
            raise ValueError(f"Error loading file: {e}")
