import pytest
from file_loader.pdf_loader import PDFLoader
from unittest.mock import patch

@pytest.fixture
def pdf_loader():
    return PDFLoader("testing/testing.py")

def test_load_small_pdf_file(pdf_loader):
    small_pdf_path = "test_files/pdf/small.pdf"
    assert pdf_loader.load_file(small_pdf_path), f"Loaded PDF file: {small_pdf_path}"

def test_load_large_pdf_file(pdf_loader):
    large_pdf_path = "test_files/pdf/large.pdf"
    assert pdf_loader.load_file(large_pdf_path), f"Loaded PDF file: {large_pdf_path}"

def test_load_corrupted_pdf_file(pdf_loader):
    corrupted_pdf_path = "test_files/pdf/corrupted.pdf"
    with pytest.raises(SystemExit):
        pdf_loader.load_file(corrupted_pdf_path)

def test_load_non_pdf_file(pdf_loader):
    non_pdf_path = "test_files/docx/sample.docx"
    with pytest.raises(SystemExit):
        pdf_loader.load_file(non_pdf_path)

def test_load_empty_pdf_file(pdf_loader):
    empty_pdf_path = "test_files/pdf/empty.pdf"
    assert pdf_loader.load_file(empty_pdf_path), f"Loaded PDF file: {empty_pdf_path}"

def test_load_password_protected_pdf(pdf_loader):
    protected_pdf_path = "test_files/pdf/protected.pdf"
    with pytest.raises(SystemExit):
        pdf_loader.load_file(protected_pdf_path)

def test_load_pdf_with_images(pdf_loader):
    pdf_with_images_path = "test_files/pdf/images.pdf"
    assert pdf_loader.load_file(pdf_with_images_path), f"Loaded PDF file: {pdf_with_images_path}"

def test_load_pdf_with_links(pdf_loader):
    pdf_with_links_path = "test_files/pdf/links.pdf"
    assert pdf_loader.load_file(pdf_with_links_path), f"Loaded PDF file: {pdf_with_links_path}"

def test_load_pdf_with_multiple_pages(pdf_loader):
    multi_page_pdf_path = "test_files/pdf/multipage.pdf"
    assert pdf_loader.load_file(multi_page_pdf_path), f"Loaded PDF file: {multi_page_pdf_path}"

def test_load_pdf_with_annotations(pdf_loader):
    annotated_pdf_path = "test_files/pdf/annotated.pdf"
    assert pdf_loader.load_file(annotated_pdf_path), f"Loaded PDF file: {annotated_pdf_path}"
