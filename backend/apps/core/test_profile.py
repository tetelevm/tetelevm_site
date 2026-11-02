from __future__ import annotations

from copy import deepcopy

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import Client
from django.urls import reverse

from apps.projects.models import Post, PostFile, Project

from .maintenance import find_orphan_files
from .models import File, FileType, Profile
from .profile_schema import flatten_content

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
            key: {"label": key, "value": "", "url": ""}
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
    url = reverse("admin:core_profile_change", args=[profile.pk])
    response = client.get(url)
    assert response.status_code == (200 if role == "admin" else 302)
    if role == "admin":
        fields = response.context["adminform"].form.fields
        assert "data" not in fields
        assert {
            "name",
            "photoFile",
            "resumeFile",
            "resumePreviewFile",
            "telegram_url",
            "lookingForWork",
            "footerCredit",
        } <= fields.keys()
    data = flatten_content(profile.data)
    data.update(
        language="ru",
        name="Новое имя",
        photoFile="",
        resumeFile="",
        resumePreviewFile="",
    )
    data.pop("lookingForWork")
    response = client.post(url, data)
    assert response.status_code == 302
    profile.refresh_from_db()
    assert profile.data["name"] == (
        "Новое имя" if role == "admin" else "Михаил Тетелев"
    )
    assert profile.data["lookingForWork"] is (role != "admin")


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
    assert data["resumeUrl"] == resume.link
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
