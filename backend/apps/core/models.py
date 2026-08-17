from __future__ import annotations

import uuid
from io import BytesIO
from pathlib import Path
from typing import Any

from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image, ImageOps, UnidentifiedImageError

PREVIEW_MAX_SIZE = (600, 600)
THUMBNAIL_SIZE = (150, 150)
PHOTO_SUFFIXES = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".webp"}
VIDEO_SUFFIXES = {".m4v", ".mov", ".mp4", ".ogv", ".webm"}
AUDIO_SUFFIXES = {".aac", ".flac", ".m4a", ".mp3", ".ogg", ".opus", ".wav"}


class FileType(models.TextChoices):
    PHOTO = "photo", _("Photo")
    VIDEO = "video", _("Video")
    AUDIO = "audio", _("Audio")
    OTHER = "other", _("Other")


def detect_file_type(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix in PHOTO_SUFFIXES:
        return FileType.PHOTO
    if suffix in VIDEO_SUFFIXES:
        return FileType.VIDEO
    if suffix in AUDIO_SUFFIXES:
        return FileType.AUDIO
    return FileType.OTHER


def file_upload_path(instance: File, filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    return f"content/{instance.id}{suffix}"


def preview_upload_path(instance: File, filename: str) -> str:
    return f"preview/{instance.id}.jpg"


def thumbnail_upload_path(instance: File, filename: str) -> str:
    return f"thumbnail/{instance.id}.jpg"


def jpeg_content(image: Image.Image) -> ContentFile:
    if image.mode in {"RGBA", "LA"}:
        background = Image.new("RGB", image.size, "white")
        alpha = image.getchannel("A")
        background.paste(image.convert("RGB"), mask=alpha)
        image = background
    elif image.mode != "RGB":
        image = image.convert("RGB")

    output = BytesIO()
    image.save(output, format="JPEG", quality=85, optimize=True)
    return ContentFile(output.getvalue())


class File(models.Model):
    id = models.UUIDField(
        _("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    original_name = models.CharField(
        _("Original name"),
        max_length=255,
        blank=True,
        editable=False,
    )
    file_type = models.CharField(
        _("File type"),
        max_length=16,
        choices=FileType.choices,
        default=FileType.OTHER,
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
    thumbnail = models.ImageField(
        _("Thumbnail"),
        upload_to=thumbnail_upload_path,
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

    @property
    def link_small(self) -> str:
        return self.thumbnail.url if self.thumbnail else self.link

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.content and not self.content._committed:
            self.original_name = Path(self.content.name).name
            self.file_type = detect_file_type(self.content.name)
        if (
            self.content
            and self.file_type == FileType.PHOTO
            and (not self.preview or not self.thumbnail)
        ):
            self._generate_images()
        super().save(*args, **kwargs)

    def _generate_images(self) -> None:
        try:
            self.content.open("rb")
            with Image.open(self.content) as source:
                image = ImageOps.exif_transpose(source)
                preview = image.copy()
                preview.thumbnail(PREVIEW_MAX_SIZE, Image.Resampling.LANCZOS)
                thumbnail = ImageOps.fit(
                    image,
                    THUMBNAIL_SIZE,
                    method=Image.Resampling.LANCZOS,
                    centering=(0.5, 0.5),
                )
        except (OSError, UnidentifiedImageError):
            return
        finally:
            content_file = getattr(self.content, "_file", None)
            if content_file is not None and not content_file.closed:
                content_file.seek(0)

        if not self.preview:
            self.preview.save(f"{self.id}.jpg", jpeg_content(preview), save=False)
        if not self.thumbnail:
            self.thumbnail.save(
                f"{self.id}.jpg",
                jpeg_content(thumbnail),
                save=False,
            )

    def __str__(self) -> str:
        return self.original_name or str(self.id)
