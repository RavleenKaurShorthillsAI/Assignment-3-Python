from PyPDF2 import PdfReader
import docx
from pptx.presentation import Presentation  # Correct import for Presentation

class DataExtractor:
    def __init__(self, file_loader):
        self.file_loader = file_loader
        self.content = file_loader.load_file()

    def extract_text(self):
        """Extract text and metadata from the loaded file."""
        print("Extracting text from file...")

        if isinstance(self.content, PdfReader):
            # PDF Text Extraction Logic
            text_data = ''
            metadata = []
            for page_num, page in enumerate(self.content.pages):
                text_data += page.extract_text() or ''
                metadata.append({"page": page_num + 1, "content_length": len(text_data)})
            print("Text extracted from PDF.")
            return {"text": text_data, "metadata": metadata}

        elif isinstance(self.content, docx.document.Document):
            # DOCX Text Extraction Logic
            print("Extracting text from DOCX...")
            text_data = ''
            metadata = []
            for paragraph in self.content.paragraphs:
                text_data += paragraph.text + '\n'
                metadata.append({"style": paragraph.style.name, "content_length": len(paragraph.text)})
            print("Text extracted from DOCX.")
            return {"text": text_data, "metadata": metadata}

        elif isinstance(self.content, Presentation):
            # PPT Text Extraction Logic
            print("Extracting text from PPT...")
            text_data = ''
            metadata = []
            for slide_num, slide in enumerate(self.content.slides):
                slide_text = ""
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        slide_text += shape.text + '\n'
                text_data += slide_text
                metadata.append({"slide": slide_num + 1, "content_length": len(slide_text)})
            print("Text extracted from PPT.")
            return {"text": text_data, "metadata": metadata}

        else:
            raise ValueError("Unsupported file format for text extraction.")
