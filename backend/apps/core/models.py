from __future__ import annotations

import uuid
from io import BytesIO
from pathlib import Path
from typing import Any

from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from PIL import Image, ImageOps, UnidentifiedImageError


def file_upload_path(instance: File, filename: str) -> str:
    return f"{timezone.localdate().isoformat()}_{Path(filename).name}"


def preview_upload_path(instance: File, filename: str) -> str:
    return f"{instance.id}.jpg"


class File(models.Model):
    id = models.UUIDField(
        _("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    content = models.FileField(_("Content"), upload_to=file_upload_path)
    preview = models.ImageField(
        _("Preview"),
        upload_to=preview_upload_path,
        blank=True,
        null=True,
        editable=False,
    )
    uploaded_at = models.DateTimeField(_("Uploaded at"), auto_now_add=True)

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")

    @property
    def link(self) -> str:
        return self.preview.url if self.preview else self.content.url

    @property
    def link_full(self) -> str | None:
        return self.content.url if self.preview else None

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.content and not self.preview:
            self._generate_preview()
        super().save(*args, **kwargs)

    def _generate_preview(self) -> None:
        try:
            self.content.open("rb")
            with Image.open(self.content) as source:
                image = ImageOps.exif_transpose(source)
                image.thumbnail((1200, 1200), Image.Resampling.LANCZOS)

                if image.mode in {"RGBA", "LA"}:
                    background = Image.new("RGB", image.size, "white")
                    alpha = image.getchannel("A")
                    background.paste(image.convert("RGB"), mask=alpha)
                    image = background
                elif image.mode != "RGB":
                    image = image.convert("RGB")

                output = BytesIO()
                image.save(output, format="JPEG", quality=85, optimize=True)
        except (OSError, UnidentifiedImageError):
            return
        finally:
            content_file = getattr(self.content, "_file", None)
            if content_file is not None and not content_file.closed:
                content_file.seek(0)

        self.preview.save(
            f"{self.id}.jpg",
            ContentFile(output.getvalue()),
            save=False,
        )

    def __str__(self) -> str:
        return str(self.id)
