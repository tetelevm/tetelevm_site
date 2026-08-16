import json
import tempfile
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import File


class FileModelTests(TestCase):
    def test_image_derivatives_have_expected_sizes_and_paths(self) -> None:
        source = BytesIO()
        Image.new("RGB", (1800, 1200), "red").save(source, format="JPEG")

        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root, MEDIA_URL="/files/"):
                uploaded = File.objects.create(
                    content=SimpleUploadedFile("photo.jpg", source.getvalue())
                )

                with Image.open(uploaded.preview.path) as preview:
                    self.assertEqual(preview.size, (600, 400))
                with Image.open(uploaded.thumbnail.path) as thumbnail:
                    self.assertEqual(thumbnail.size, (150, 150))

                self.assertEqual(uploaded.original_name, "photo.jpg")
                self.assertEqual(
                    uploaded.content.name,
                    f"content/{uploaded.id}.jpg",
                )
                self.assertEqual(
                    uploaded.preview.name,
                    f"preview/{uploaded.id}.jpg",
                )
                self.assertEqual(
                    uploaded.thumbnail.name,
                    f"thumbnail/{uploaded.id}.jpg",
                )

    def test_thumbnail_upscales_small_images(self) -> None:
        source = BytesIO()
        Image.new("RGB", (60, 40), "blue").save(source, format="PNG")

        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root, MEDIA_URL="/files/"):
                uploaded = File.objects.create(
                    content=SimpleUploadedFile("small.png", source.getvalue())
                )

                with Image.open(uploaded.preview.path) as preview:
                    self.assertEqual(preview.size, (60, 40))
                with Image.open(uploaded.thumbnail.path) as thumbnail:
                    self.assertEqual(thumbnail.size, (150, 150))

    def test_non_image_uses_uuid_filename_and_has_no_derivatives(self) -> None:
        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root, MEDIA_URL="/files/"):
                uploaded = File.objects.create(
                    content=SimpleUploadedFile("Example.MOV", b"video")
                )

                self.assertEqual(uploaded.original_name, "Example.MOV")
                self.assertEqual(
                    uploaded.content.name,
                    f"content/{uploaded.id}.mov",
                )
                self.assertEqual(uploaded.link, f"/files/content/{uploaded.id}.mov")
                self.assertFalse(uploaded.preview)
                self.assertFalse(uploaded.thumbnail)
                self.assertTrue(uploaded.content.storage.exists(uploaded.content.name))


class AuthenticationApiTests(TestCase):
    def setUp(self) -> None:
        user_model = get_user_model()
        self.guest = user_model.objects.create_user("guest", password="guest-pass")
        self.admin = user_model.objects.create_superuser(
            "admin",
            password="admin-pass",
        )
        self.client = Client(enforce_csrf_checks=True)

    def csrf_token(self) -> str:
        response = self.client.get(reverse("core:csrf"))
        return response.json()["csrfToken"]

    def post_json(
        self,
        url: str,
        data: dict[str, str],
        csrf_token: str | None = None,
    ) -> HttpResponse:
        headers = {"HTTP_X_CSRFTOKEN": csrf_token} if csrf_token else {}
        return self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json",
            **headers,
        )

    def test_anonymous_session(self) -> None:
        response = self.client.get(reverse("core:session"))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["isAuthenticated"])

    def test_login_requires_csrf(self) -> None:
        response = self.post_json(
            reverse("core:login"),
            {"username": "guest", "password": "guest-pass"},
        )

        self.assertEqual(response.status_code, 403)

    def test_invalid_credentials_are_rejected(self) -> None:
        response = self.post_json(
            reverse("core:login"),
            {"username": "guest", "password": "wrong"},
            self.csrf_token(),
        )

        self.assertEqual(response.status_code, 401)

    def test_guest_can_login_and_logout(self) -> None:
        login_response = self.post_json(
            reverse("core:login"),
            {"username": "guest", "password": "guest-pass"},
            self.csrf_token(),
        )

        self.assertEqual(login_response.status_code, 200)
        self.assertFalse(login_response.json()["isStaff"])
        session_response = self.client.get(reverse("core:session"))
        self.assertTrue(session_response.json()["isAuthenticated"])

        logout_response = self.post_json(
            reverse("core:logout"),
            {},
            self.csrf_token(),
        )
        self.assertEqual(logout_response.status_code, 200)
        session_response = self.client.get(reverse("core:session"))
        self.assertFalse(session_response.json()["isAuthenticated"])

    def test_admin_can_login(self) -> None:
        response = self.post_json(
            reverse("core:login"),
            {"username": "admin", "password": "admin-pass"},
            self.csrf_token(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["isStaff"])

    def test_logout_requires_csrf(self) -> None:
        self.client.force_login(self.guest)

        response = self.post_json(reverse("core:logout"), {})

        self.assertEqual(response.status_code, 403)
