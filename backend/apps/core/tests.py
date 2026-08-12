import tempfile
from datetime import date
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from .models import File


class FileModelTests(TestCase):
    def test_upload_uses_date_and_original_filename(self) -> None:
        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root, MEDIA_URL="/files/"):
                with patch(
                    "apps.core.models.timezone.localdate",
                    return_value=date(2026, 8, 12),
                ):
                    uploaded = File.objects.create(
                        content=SimpleUploadedFile("Example.MOV", b"video")
                    )

                self.assertEqual(uploaded.content.name, "2026-08-12_Example.MOV")
                self.assertEqual(uploaded.link, "/files/2026-08-12_Example.MOV")
                self.assertTrue(uploaded.content.storage.exists(uploaded.content.name))
