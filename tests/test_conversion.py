from pathlib import Path

import pytest
from PIL import Image
from django.core.exceptions import ObjectDoesNotExist

from pdf_convertor_app.io_helpers import get_converted_path, get_upload_path
from pdf_convertor_app.models import Document
from pdf_convertor_app.tasks import render_pdf_pages

_pdf_root = Path(__file__).parent / 'resources'


class MockChunkedFile:
    def __init__(self, path: str):
        self._path = _pdf_root / path

    def chunks(self):
        with self._path.open("rb") as f:
            yield f.read()

    def assert_file_is_same(self, other: Path):
        reference = None
        with self._path.open("rb") as f:
            reference = f.read()

        with other.open("rb") as f:
            assert reference == f.read()


def assert_images_ok(doc_id, expected_pages):
    doc = get_record(doc_id)

    assert doc.pages == expected_pages
    assert not get_converted_path(doc_id, expected_pages + 1).exists()
    assert not get_converted_path(doc_id, 0).exists()
    for page in range(1, doc.pages):
        file = get_converted_path(doc_id, page)
        assert file.exists()
        assert file.suffix == '.png'
        with Image.open(file) as f:
            x, y = f.size
            assert x <= 1200
            assert y <= 1600


def get_record(doc_id) -> Document:
    return Document.objects.get(pk=doc_id)


def test_saving(transactional_db):
    mock_file = MockChunkedFile("test.pdf")

    doc_id = Document.save_file(mock_file)

    mock_file.assert_file_is_same(get_upload_path(doc_id))
    assert get_record(doc_id)


@pytest.mark.parametrize("path,pages", [
    ("test.pdf", 24),
    ("test-landscape.pdf", 1),
    ("test-no-ext", 1)
])
def test_conversion(transactional_db, path, pages):
    mock_file = MockChunkedFile(path)

    doc_id = Document.save_file(mock_file)
    render_pdf_pages(doc_id)

    assert_images_ok(doc_id, pages)
    assert not get_upload_path(doc_id).exists()


def test_non_pdf(transactional_db):
    mock_file = MockChunkedFile("nonpdf.pdf")

    doc_id = Document.save_file(mock_file)
    render_pdf_pages(doc_id)
    with pytest.raises(ObjectDoesNotExist):
        get_record(doc_id)

# todo add api test
