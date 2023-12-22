import uuid

from django.db import models
from django.db import transaction

from .io_helpers import get_upload_path


class Document(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    done = models.BooleanField(default=False)
    pages = models.IntegerField(default=-1)

    @classmethod
    def save_file(cls, file) -> str:
        """IRL this would go somewhere else like S3 """

        with transaction.atomic():
            # noinspection PyUnresolvedReferences
            document = cls.objects.create()
            target_path = get_upload_path(document.id)
            try:
                with target_path.open("wb") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                document.save()
            except Exception:
                target_path.unlink(missing_ok=True)
                raise

        return document.id
