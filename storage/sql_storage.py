import mysql.connector
from mysql.connector import Error
import os

class SQLStorage:
    """
    SQLStorage class responsible for storing extracted data in a MySQL database.
    Handles the connection, table creation, and data insertion.
    """

    def __init__(self, db_config):
        """
        Initialize the SQLStorage class with database configuration and create a connection.
        :param db_config: Dictionary containing database configuration (user, password, host, database).
        """
        self.db_config = db_config
        self.connection = None
        self.create_connection()  # Ensure connection is established when the class is instantiated

    def create_connection(self):
        """
        Create a database connection using the MySQL connector.
        """
        try:
            # Connect to the MySQL database using provided configuration
            connection = mysql.connector.connect(
                user=self.db_config['user'],
                password=self.db_config['password'],
                host=self.db_config['host'],
                database=self.db_config['database']
            )
            # Check if the connection is successfully established
            if connection.is_connected():
                self.connection = connection
                print("Connection to MySQL established")
        except mysql.connector.Error as e:
            # Handle connection errors
            print(f"Error connecting to MySQL: {e}")
            self.connection = None

    def create_tables(self):
        """
        Create tables in the MySQL database for storing extracted data.
        Creates tables for files, texts, tables, images, metadata, and links.
        """
        if self.connection is None:
            print("No database connection. Cannot create tables.")
            return

        # SQL statements for creating the necessary tables
        create_statements = [
            """
            CREATE TABLE IF NOT EXISTS extracted_files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255) NOT NULL,
                file_type VARCHAR(50),
                extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS extracted_texts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_id INT,
                text LONGTEXT,
                FOREIGN KEY (file_id) REFERENCES extracted_files(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS extracted_tables (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_id INT,
                table_data LONGTEXT,
                FOREIGN KEY (file_id) REFERENCES extracted_files(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS extracted_images (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_id INT,
                image_path VARCHAR(255),
                FOREIGN KEY (file_id) REFERENCES extracted_files(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS extracted_metadata (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_id INT,
                metadata_key VARCHAR(255),
                metadata_value TEXT,
                FOREIGN KEY (file_id) REFERENCES extracted_files(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS extracted_links (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_id INT,
                link VARCHAR(255),
                FOREIGN KEY (file_id) REFERENCES extracted_files(id)
            )
            """
        ]

        cursor = self.connection.cursor()  # Create a cursor for executing SQL statements
        try:
            # Execute each SQL statement to create the tables
            for statement in create_statements:
                cursor.execute(statement)
            self.connection.commit()  # Commit the changes to the database
            print("Tables created successfully.")
        except Error as e:
            # Handle errors during table creation
            print(f"Error creating tables: {e}")
        finally:
            cursor.close()  # Close the cursor after executing statements

    def store_data(self, extractor):
        """
        Store the extracted data (text, tables, images, metadata, and links) into the database.
        :param extractor: An instance of UniversalDataExtractor that extracts data from files.
        """
        if self.connection is None:
            print("No database connection. Cannot store data.")
            return

        file_name = extractor.get_file_name()  # Get the name of the file being processed
        file_type = extractor.__class__.__name__  # Get the class name of the extractor (for file type)

        cursor = self.connection.cursor()  # Create a cursor for executing SQL statements
        try:
            # Insert the file information into the extracted_files table
            cursor.execute(
                "INSERT INTO extracted_files (file_name, file_type) VALUES (%s, %s)",
                (file_name, file_type)
            )
            file_id = cursor.lastrowid  # Get the ID of the newly inserted file

            # Store extracted text
            text = extractor.extract_text()
            if text:
                cursor.execute(
                    "INSERT INTO extracted_texts (file_id, text) VALUES (%s, %s)",
                    (file_id, text)
                )

            # Store extracted tables
            tables = extractor.extract_tables()
            for table in tables:
                table_data = '\n'.join([','.join(row) for row in table])  # Format table data as CSV-like string
                cursor.execute(
                    "INSERT INTO extracted_tables (file_id, table_data) VALUES (%s, %s)",
                    (file_id, table_data)
                )

            # Store extracted images (paths to the images saved locally)
            images = extractor.extract_images()
            for image_path in images:
                cursor.execute(
                    "INSERT INTO extracted_images (file_id, image_path) VALUES (%s, %s)",
                    (file_id, image_path)
                )

            # Store extracted metadata as key-value pairs
            metadata = extractor.extract_metadata()
            if isinstance(metadata, dict):
                for key, value in metadata.items():
                    if value:  # Store non-empty metadata values
                        cursor.execute(
                            "INSERT INTO extracted_metadata (file_id, metadata_key, metadata_value) VALUES (%s, %s, %s)",
                            (file_id, key, value)
                        )

            # Store extracted hyperlinks
            links = extractor.extract_links()
            for link in links:
                cursor.execute(
                    "INSERT INTO extracted_links (file_id, link) VALUES (%s, %s)",
                    (file_id, link)
                )

            self.connection.commit()  # Commit all the data insertions
            print("Data stored successfully.")

        except Error as e:
            # Handle errors during data storage and rollback changes
            print(f"Error storing data: {e}")
            self.connection.rollback()
        finally:
            cursor.close()  # Close the cursor after the data is stored

    def close_connection(self):
        """
        Close the database connection if it is still open.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")
