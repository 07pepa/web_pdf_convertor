import uuid

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from .io_helpers import get_converted_path
from .models import Document
from .tasks import render_pdf_pages


def _get_doc(pk):
    return get_object_or_404(Document, pk=pk)


@api_view(['POST'])
@parser_classes([FileUploadParser])
def upload(request):
    file = request.data.get("file")
    if not file:
        return Response({"error": "No file provided."}, status=400)
    doc_id = str(Document.save_file(file))
    render_pdf_pages.send(doc_id)
    return Response({"id": doc_id}, status=201)


@api_view(["GET"])
def status(_, doc_id: uuid):
    """
    undocumented and not required but reasonable features
    while document is still processing n_pages is -1 to adhere predefined
    it is also undefined what to do in case where non pdf is uploaded
    I opted for let's just forget it, so it may go from processing to respond with 404
    """
    document = _get_doc(doc_id)
    text_status = "done" if document.done else "processing"
    return Response({"status": text_status, "n_pages": document.pages})


@api_view(["GET"])
def rendered_page(_, doc_id, page_num):
    document = _get_doc(doc_id)
    if document.done:
        page_number = int(page_num)
        path = get_converted_path(document.id, page_number)
        return FileResponse(path.open("rb"))
    else:
        return Response({"error": "Document is still processing."}, status=425)
