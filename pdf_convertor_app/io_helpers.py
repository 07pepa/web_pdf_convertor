import os
import uuid
from pathlib import Path
from typing import Final

_upload_root: Final = Path(os.getenv("UPLOAD_ROOT")).resolve()

_converted_root: Final = Path(os.getenv("CONVERTED_ROOT")).resolve()
# ensure path exist
_upload_root.mkdir(0o700, parents=True, exist_ok=True)
_converted_root.mkdir(0o700, parents=True, exist_ok=True)


# this is simplification  in reality i, would use s3 or something like object db to store binary files
def get_upload_path(doc_id: uuid) -> Path:
    return _upload_root / f"{doc_id}.pdf"


def get_converted_path(doc_id: uuid, page: int) -> Path:
    return _converted_root / f"{doc_id}_page_{page}.png"
