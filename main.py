from file_loader.pdf_loader import PDFLoader
from file_loader.docx_loader import DOCXLoader
from file_loader.ppt_loader import PPTLoader
from data_extractor.data_extractor import DataExtractor

def test_pdf():
    pdf_loader = PDFLoader('samples/Sample_file.pdf')  # Make sure the file path is correct
    extractor = DataExtractor(pdf_loader)
    text_data = extractor.extract_text()
    print("PDF Text Data:", text_data)

def test_docx():
    docx_loader = DOCXLoader('samples/Sample_file.docx')  # Make sure the file path is correct
    extractor = DataExtractor(docx_loader)
    text_data = extractor.extract_text()
    print("DOCX Text Data:", text_data)

def test_ppt():
    ppt_loader = PPTLoader('samples/Sample_file.pptx')  # Make sure the file path is correct
    extractor = DataExtractor(ppt_loader)
    text_data = extractor.extract_text()
    print("PPT Text Data:", text_data)

if __name__ == '__main__':
    test_pdf()  # Test PDF extraction
    test_docx()  # Test DOCX extraction
    test_ppt()  # Test PPT extraction
