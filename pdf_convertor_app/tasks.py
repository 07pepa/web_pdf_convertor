import fitz  # PyMuPDF
import magic
from PIL import Image
from django.db import transaction
from dramatiq import actor

from .io_helpers import get_converted_path, get_upload_path
from .models import Document

max_size = (1200, 1600)


@actor(max_retries=3)
def render_pdf_pages(document_id):
    # noinspection PyUnresolvedReferences
    document = Document.objects.get(pk=document_id)
    pdf_path = get_upload_path(document_id)
    if not document:  # check if exist in db (converting something that is unreferenced is undefined better delete it
        pdf_path.unlink(missing_ok=True)
        return

    # fast check (could be done on api side but may have issue with scaling)
    if magic.from_file(str(pdf_path), mime=True) != "application/pdf":
        document.delete()  # just ignore spam pretend we never accepted such document
        pdf_path.unlink(missing_ok=True)  # delete spam
        return
    page_num = 1
    # noinspection PyUnresolvedReferences
    with fitz.open(pdf_path) as pdf:
        page_count = len(pdf)
        for page in range(0, page_count):
            page = pdf.load_page(page)
            bit_image = page.get_pixmap()
            pil_image = Image.frombytes("RGB", (bit_image.width, bit_image.height), bit_image.samples)
            pil_image.thumbnail(max_size, Image.LANCZOS)
            path = get_converted_path(document_id, page_num)
            pil_image.save(path, "PNG")
            page_num += 1

    pdf_path.unlink()

    with transaction.atomic():
        document.done = True
        document.pages = page_count
        document.save()
