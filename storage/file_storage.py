import os
import csv
from data_extractor.data_extractor import UniversalDataExtractor
from file_loader.concrete_file_loader import Loader

from PIL import Image
import io
from tabulate import tabulate  # Importing tabulate for pretty table display

class FileStorage:
    """
    FileStorage class is responsible for storing extracted data from a file
    (e.g., text, tables, images, metadata, and links) into a directory structure.
    """

    def __init__(self, output_dir):
        """
        Initialize the FileStorage with an output directory where all the extracted
        data will be saved.
        
        :param output_dir: The base directory where the extracted files will be stored.
        """
        self.output_dir = output_dir

    def store_data(self, extractor):
        """
        Store data extracted by the extractor.
        Creates directories for storing text, tables, images, metadata, and links.
        
        :param extractor: An instance of UniversalDataExtractor that handles data extraction.
        """
        # Create a directory for storing extracted files (named after the original file)
        base_folder = os.path.join(self.output_dir, extractor.get_file_name())
        os.makedirs(base_folder, exist_ok=True)  # Create the directory if it doesn't exist

        # Extract and store text data
        data = extractor.extract_text()

        if data and 'text' in data and data['text'].strip():
            text_file_path = os.path.join(base_folder, "extracted_text.txt")
            
            # Write the extracted text data to a file
            with open(text_file_path, 'w', encoding='utf-8') as text_file:
                text_file.write(data['text'])
            print(f"Text data saved to {text_file_path}")
        # else:
        #     print("No text data found.")  # You can enable this if no text is found

        # Extract and store table data
        tables = extractor.extract_tables()
        if tables:
            # Create a folder for tables
            tables_folder = os.path.join(base_folder, "tables")
            os.makedirs(tables_folder, exist_ok=True)
            for i, table in enumerate(tables):
                csv_file_path = os.path.join(tables_folder, f"table_{i + 1}.csv")
                # Save each table as a CSV file
                with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(table)  # Write the rows of the table to CSV
                print(f"Table data saved to {csv_file_path}")
                # Optionally display the table in the terminal
                # print(f"Table {i + 1}:\n{tabulate(table, headers='keys', tablefmt='grid')}")
        else:
            print("No tables extracted.")

        # Extract and store images
        images = extractor.extract_images()
        if images:
            # Create a folder for images
            images_folder = os.path.join(base_folder, "images")
            os.makedirs(images_folder, exist_ok=True)
            for i, img_info in enumerate(images):
                # Check if the image data is valid and contains a stream
                if isinstance(img_info, dict) and 'stream' in img_info:
                    img_stream = img_info['stream']
                    img_data = img_stream.get_rawdata()

                    # Convert PDFStream to a Pillow image and save as PNG
                    try:
                        img = Image.open(io.BytesIO(img_data))
                        img_path = os.path.join(images_folder, f"image_{i + 1}.png")
                        img.save(img_path)
                        print(f"Image saved to {img_path}")
                    except Exception as e:
                        print(f"Error saving image {i + 1}: {e}")
                else:
                    print(f"Image data for image {i + 1} is not valid or not found.")

        # Extract and store general metadata
        metadata = extractor.extract_metadata()
        if metadata:
            metadata_file_path = os.path.join(base_folder, "metadata.txt")
            with open(metadata_file_path, 'w', encoding='utf-8') as metadata_file:
                if isinstance(metadata, dict):
                    # Save non-empty metadata key-value pairs
                    for key, value in metadata.items():
                        if value:
                            metadata_file.write(f"{key}: {value}\n")
                else:
                    # Save non-empty attributes of the metadata object
                    for prop in dir(metadata):
                        if not prop.startswith('_') and prop != 'xml':
                            value = getattr(metadata, prop)
                            if value:
                                metadata_file.write(f"{prop}: {value}\n")
            print(f"Metadata saved to {metadata_file_path}")
        else:
            print("No metadata extracted.")

        # Extract and store links
        links = extractor.extract_links()
        unique_links = set(filter(None, links))  # Remove empty links and duplicates
        if unique_links:
            links_file_path = os.path.join(base_folder, "extracted_links.txt")
            # Write the unique links to a file
            with open(links_file_path, 'w', encoding='utf-8') as links_file:
                for link in unique_links:
                    links_file.write(f"{link}\n")
            print(f"Links data saved to {links_file_path}")
        else:
            print("No links extracted.")
