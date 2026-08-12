from __future__ import annotations

import uuid
from pathlib import Path

from django.db import models
from django.utils import timezone


def file_upload_path(instance: File, filename: str) -> str:
    return f"{timezone.localdate().isoformat()}_{Path(filename).name}"


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.FileField(upload_to=file_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def link(self) -> str:
        return self.content.url

    def __str__(self) -> str:
        return str(self.id)
