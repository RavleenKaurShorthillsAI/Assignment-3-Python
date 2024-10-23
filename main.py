import os
from dotenv import load_dotenv
from data_extractor.data_extractor import UniversalDataExtractor
from file_loader.concrete_file_loader import Loader  # Import the common Loader class
from storage.file_storage import FileStorage
from storage.sql_storage import SQLStorage
from tabulate import tabulate  # Used for formatting tabular data, if needed later

class Main:
    def __init__(self):
        # Load environment variables from a .env file (used for sensitive information like database credentials)
        load_dotenv()
        
        # Database configuration dictionary populated with values from environment variables
        self.db_config = {
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME')
        }
        
        # Initialize file storage (for saving extracted data in files)
        self.file_storage = FileStorage("output")  # Data will be saved in the "output" directory
        
        # Initialize SQL storage (for saving extracted data in the database using the configuration from .env)
        self.sql_storage = SQLStorage(self.db_config)
        
        # Create database tables if they don't already exist
        self.sql_storage.create_tables()

    def get_user_file_path(self):
        """Prompt the user for a file path and return it."""
        file_path = input("Please enter the file path: ")
        return file_path

    def process_file(self, file_path, file_type):
        """
        Load, extract, store, and print data using the common Loader.
        This method handles the file loading, extraction, and storage processes.
        """
        
        # Create an instance of the Loader class, which loads files based on their type (PDF, DOCX, PPTX, etc.)
        loader = Loader(file_path, file_type)
        
        # Load the file based on the file type (handled inside the Loader class)
        loader.load_file()
        
        # Create an instance of UniversalDataExtractor, which performs text, image, link, table extraction on the loaded file
        extractor = UniversalDataExtractor(loader)
        
        # Store the extracted data in files (using FileStorage)
        self.file_storage.store_data(extractor)
        
        # Store the extracted data in a database (using SQLStorage)
        self.sql_storage.store_data(extractor)

    def run(self):
        """Main function that runs the application, handles user input, and processes the file."""
        
        # Get the file path from the user
        file_path = self.get_user_file_path()

        # Extract the file type (extension) from the provided file path
        file_type = os.path.splitext(file_path)[1][1:]  # Extract extension without the dot
        
        # Check if the file type is supported
        if file_type:
            # Process the file using the common Loader and UniversalDataExtractor
            self.process_file(file_path, file_type)
        else:
            # If the file format is not supported, print an error message
            print("File format not supported. Please provide a .pdf, .docx, or .pptx file.")

if __name__ == "__main__":
    # Create an instance of the Main class and run the application
    main_instance = Main()
    main_instance.run()
