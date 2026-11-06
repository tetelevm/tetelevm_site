from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from urllib.parse import quote

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, override_settings
from django.urls import reverse

from apps.projects.models import Post, PostFile, Project

from .maintenance import find_orphan_files
from .models import File, FileType, Profile
from .profile_schema import ProfileContentForm, flatten_content

pytestmark = pytest.mark.django_db


@pytest.fixture
def profile() -> Profile:
    data = {
        "name": "Михаил Тетелев",
        "role": "Python developer",
        "about": "Test biography",
        "lookingForWork": True,
        "photoFile": None,
        "resumeFile": None,
        "contacts": {
            key: {"value": "", "url": ""}
            for key in (
                "telegram",
                "email",
                "linkedin",
                "github",
                "channel",
                "instagram",
                "linktree",
            )
        },
    }
    return Profile.objects.create(language="ru", data=data)


def login_role(client: Client, role: str) -> None:
    if role != "anonymous":
        client.force_login(
            get_user_model().objects.create_user(
                role, is_staff=role == "admin", is_superuser=role == "admin"
            )
        )


@pytest.mark.parametrize("role", ["anonymous", "guest", "admin"])
def test_public_read_only_api(client: Client, role: str, profile: Profile) -> None:
    login_role(client, role)
    url = reverse("profile", args=["ru"])
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["name"] == "Михаил Тетелев"
    assert response.json()["photoUrl"] is None
    assert response.json()["resumePreviewUrl"] is None
    assert "availabilityText" not in response.json()
    assert "label" not in response.json()["contacts"]["telegram"]
    for method in ("post", "put", "patch", "delete"):
        assert (
            getattr(client, method)(
                url, data={}, content_type="application/json"
            ).status_code
            == 405
        )
    profile.refresh_from_db()
    assert profile.data["name"] == "Михаил Тетелев"


def test_language_selection_and_missing_profile(
    client: Client, profile: Profile
) -> None:
    english = deepcopy(profile.data)
    english["name"] = "English name"
    Profile.objects.update_or_create(language="en", defaults={"data": english})
    assert client.get(reverse("profile", args=["en"])).json()["name"] == "English name"
    assert (
        client.get(reverse("profile", args=["ru"])).json()["name"] == "Михаил Тетелев"
    )
    assert client.get(reverse("profile", args=["de"])).status_code == 404
    Profile.objects.filter(language="en").delete()
    assert client.get(reverse("profile", args=["en"])).status_code == 404


@pytest.mark.parametrize("role", ["anonymous", "guest", "admin"])
def test_admin_structured_form_permissions(
    client: Client, role: str, profile: Profile
) -> None:
    login_role(client, role)
    search = client.get(
        reverse("admin:autocomplete"),
        {
            "app_label": "projects",
            "model_name": "postfile",
            "field_name": "file",
            "term": "private file",
        },
    )
    assert search.status_code == (200 if role == "admin" else 302)
    url = reverse("admin:core_profile_change", args=[profile.pk])
    response = client.get(url)
    assert response.status_code == (200 if role == "admin" else 302)
    if role == "admin":
        fields = response.context["adminform"].form.fields
        assert "data" not in fields
        assert "footerCredit" not in fields
        assert "telegram_label" not in fields
        assert {
            "name",
            "photoFile",
            "resumeFile",
            "resumeFilename",
            "resumePreviewFile",
            "telegram_url",
            "lookingForWork",
        } <= fields.keys()
    data = flatten_content(profile.data)
    data.update(
        language="ru",
        name="Новое имя",
        photoFile="",
        resumeFile="",
        resumePreviewFile="",
        resumeFilename="Новое_резюме.pdf",
    )
    data.pop("lookingForWork")
    response = client.post(url, data)
    assert response.status_code == 302
    profile.refresh_from_db()
    assert profile.data["name"] == (
        "Новое имя" if role == "admin" else "Михаил Тетелев"
    )
    assert profile.data["lookingForWork"] is (role != "admin")
    assert profile.data.get("resumeFilename", "") == (
        "Новое_резюме.pdf" if role == "admin" else ""
    )


def test_admin_csrf_and_validation(profile: Profile) -> None:
    client = Client(enforce_csrf_checks=True)
    client.force_login(
        get_user_model().objects.create_superuser("admin", password="test")
    )
    url = reverse("admin:core_profile_change", args=[profile.pk])
    assert client.post(url, {}).status_code == 403
    assert client.get(url).status_code == 200
    data = flatten_content(profile.data)
    data.update(
        language="ru",
        photoFile="",
        resumeFile="",
        resumePreviewFile="",
        telegram_url="javascript:alert(1)",
        csrfmiddlewaretoken=client.cookies["csrftoken"].value,
    )
    response = client.post(url, data)
    assert response.status_code == 200
    assert "telegram_url" in response.context["adminform"].form.errors
    profile.refresh_from_db()
    assert profile.data["contacts"]["telegram"]["url"] == ""


def test_invalid_profile_structure_is_rejected(profile: Profile) -> None:
    profile.data["lookingForWork"] = "false"
    with pytest.raises(ValidationError):
        profile.save()
    profile.data = {"contacts": []}
    with pytest.raises(ValidationError):
        profile.save()


def test_file_types_and_urls(client: Client, profile: Profile) -> None:
    photo = File.objects.create(content="content/photo.jpg", file_type=FileType.PHOTO)
    resume = File.objects.create(content="content/resume.pdf")
    profile.data.update(
        photoFile=str(photo.pk),
        resumePreviewFile=str(photo.pk),
        resumeFile=str(resume.pk),
    )
    profile.data["contacts"]["email"]["url"] = "hello@example.com"
    profile.save()
    data = client.get(reverse("profile", args=["ru"])).json()
    assert data["photoUrl"] == photo.link
    assert data["resumeUrl"] == reverse("profile-resume", args=["ru"])
    assert data["resumePreviewUrl"] == photo.link
    assert data["contacts"]["email"]["url"] == "mailto:hello@example.com"
    profile.data["resumePreviewFile"] = str(resume.pk)
    with pytest.raises(ValidationError):
        profile.save()
    profile.data["resumePreviewFile"] = None
    profile.data["photoFile"] = str(resume.pk)
    with pytest.raises(ValidationError):
        profile.save()
    profile.data.update(photoFile=None, resumeFile=str(photo.pk))
    with pytest.raises(ValidationError):
        profile.save()


@pytest.mark.parametrize("role", ["anonymous", "guest", "admin"])
@pytest.mark.parametrize(
    ("language", "filename"),
    [
        ("ru", "Михаил_Тетелев_CV.pdf"),
        ("en", "Mikhail_Tetelev_CV.pdf"),
        ("ru", ""),
    ],
)
def test_resume_filename_and_public_access(
    client: Client, profile: Profile, tmp_path: Path,
    role: str, language: str, filename: str,
) -> None:
    login_role(client, role)
    pdf_bytes = b"%PDF-1.4\nTest resume"
    with override_settings(MEDIA_ROOT=tmp_path):
        pdf = File.objects.create(
            content=SimpleUploadedFile("original.pdf", pdf_bytes)
        )
        profile.language = language
        profile.data["resumeFile"] = str(pdf.pk)
        profile.data["resumeFilename"] = filename
        profile.save()
        url = client.get(reverse("profile", args=[language])).json()["resumeUrl"]
        assert url == reverse("profile-resume", args=[language])
        response = client.get(url)
        assert response.status_code == 200
        assert response["Content-Type"] == "application/pdf"
        filename = filename or "resume.pdf"
        disposition = (
            f'inline; filename="{filename}"' if filename.isascii()
            else f"inline; filename*=utf-8''{quote(filename)}"
        )
        assert response["Content-Disposition"] == disposition
        assert response["Cache-Control"] == "no-store"
        assert b"".join(response.streaming_content) == pdf_bytes
        head = client.head(url)
        assert head.status_code == 200
        assert head["Content-Disposition"] == disposition
        assert b"".join(head.streaming_content) == b""
        assert client.post(url).status_code == 405


@pytest.mark.parametrize(
    "filename", ["../resume.pdf", "folder\\resume.pdf", "resume\n.pdf", "resume.txt"]
)
def test_resume_filename_validation(profile: Profile, filename: str) -> None:
    data = flatten_content(profile.data)
    data["resumeFilename"] = filename
    form = ProfileContentForm(data=data)
    assert not form.is_valid()
    assert "resumeFilename" in form.errors


def test_missing_resume_returns_404(
    client: Client, profile: Profile, tmp_path: Path,
) -> None:
    url = reverse("profile-resume", args=["ru"])
    assert client.get(url).status_code == 404
    assert client.get(reverse("profile-resume", args=["en"])).status_code == 404
    assert client.get(reverse("profile-resume", args=["de"])).status_code == 404
    with override_settings(MEDIA_ROOT=tmp_path):
        pdf = File.objects.create(content="content/missing.pdf")
        profile.data["resumeFile"] = str(pdf.pk)
        profile.save()
        assert client.get(url).status_code == 404
        pdf.delete()
        assert client.get(url).status_code == 404


def test_profile_media_can_be_retained_by_service_post(
    client: Client, profile: Profile
) -> None:
    photo = File.objects.create(content="photo.jpg", file_type=FileType.PHOTO)
    pdf = File.objects.create(content="resume.pdf")
    profile.data.update(
        photoFile=str(photo.pk), resumePreviewFile=str(photo.pk), resumeFile=str(pdf.pk)
    )
    profile.save()
    assert set(find_orphan_files()) == {photo, pdf}
    project = Project.objects.create(
        name="Service", link="service", cover=photo, is_public=False
    )
    post = Post.objects.create(project=project, number=0, is_draft=True)
    attachment = PostFile.objects.create(post=post, file=pdf)
    assert not find_orphan_files().exists()
    attachment.delete()
    assert list(find_orphan_files()) == [pdf]
    client.force_login(
        get_user_model().objects.create_superuser("admin", password="test")
    )
    assert (
        client.post(
            reverse("admin:core_file_delete", args=[pdf.pk]), {"post": "yes"}
        ).status_code
        == 302
    )
    assert client.get(reverse("profile", args=["ru"])).json()["resumeUrl"] is None


def test_profile_file_selectors_load_choices_on_demand(
    client: Client, profile: Profile
) -> None:
    photos = File.objects.bulk_create(
        [
            File(
                label=f"Candidate {index:02}",
                content=f"content/{index}.jpg",
                file_type=FileType.PHOTO,
            )
            for index in range(21)
        ]
    )
    pdf = File.objects.create(label="Resume PDF", content="content/resume.pdf")
    profile.data.update(
        photoFile=str(photos[0].pk),
        resumePreviewFile=str(photos[0].pk),
        resumeFile=str(pdf.pk),
    )
    profile.save()
    login_role(client, "admin")
    response = client.get(reverse("admin:core_profile_change", args=[profile.pk]))
    form = response.context["adminform"].form
    for name, selected in (
        ("photoFile", photos[0]),
        ("resumePreviewFile", photos[0]),
        ("resumeFile", pdf),
    ):
        html = str(form[name])
        assert "admin-autocomplete" in html
        assert selected.label in html
        assert photos[1].label not in html
        assert html.count("<option ") == 2
    params = {
        "app_label": "projects",
        "model_name": "postfile",
        "field_name": "file",
        "term": "Candidate",
    }
    response = client.get(reverse("admin:autocomplete"), params)
    assert len(response.json()["results"]) == 20
    assert response.json()["pagination"]["more"] is True
    response = client.get(reverse("admin:autocomplete"), {**params, "page": 2})
    assert len(response.json()["results"]) == 1
    response = client.get(
        reverse("admin:autocomplete"), {**params, "term": "Candidate 07"}
    )
    assert [result["id"] for result in response.json()["results"]] == [
        str(photos[7].pk)
    ]
