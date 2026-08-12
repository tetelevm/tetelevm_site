from __future__ import annotations

import uuid
from pathlib import Path

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def file_upload_path(instance: File, filename: str) -> str:
    return f"{timezone.localdate().isoformat()}_{Path(filename).name}"


class File(models.Model):
    id = models.UUIDField(
        _("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    content = models.FileField(_("Content"), upload_to=file_upload_path)
    uploaded_at = models.DateTimeField(_("Uploaded at"), auto_now_add=True)

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")

    @property
    def link(self) -> str:
        return self.content.url

    def __str__(self) -> str:
        return str(self.id)
