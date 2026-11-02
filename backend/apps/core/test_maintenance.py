from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from pytest_django.fixtures import Settings

from apps.core.maintenance import find_orphan_files, tidy_media
from apps.core.models import File
from apps.projects.maintenance import relabel_project_files
from apps.projects.models import Post, PostFile, Project

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("role", ["anonymous", "guest", "staff", "admin"])
@pytest.mark.parametrize(
    "operation", ["core_file_tidy_media", "projects_post_relabel_files"]
)
def test_maintenance_permissions(client: Client, role: str, operation: str) -> None:
    if role != "anonymous":
        user = get_user_model().objects.create_user(
            role,
            is_staff=role in {"staff", "admin"},
            is_superuser=role == "admin",
        )
        client.force_login(user)
    target = (
        "apps.core.admin.tidy_media"
        if operation == "core_file_tidy_media"
        else "apps.projects.admin.relabel_project_files"
    )
    url = reverse(f"admin:{operation}")
    with patch(target, return_value=0) as run:
        response = client.get(url)
        assert response.status_code == (
            200 if role == "admin" else 403 if role == "staff" else 302
        )
        run.assert_not_called()
        response = client.post(url)
        assert response.status_code == (403 if role == "staff" else 302)
        assert run.call_count == (1 if role == "admin" else 0)


@pytest.mark.parametrize(
    "operation", ["core_file_tidy_media", "projects_post_relabel_files"]
)
def test_maintenance_requires_csrf(operation: str) -> None:
    client = Client(enforce_csrf_checks=True)
    client.force_login(
        get_user_model().objects.create_superuser("admin", password="test")
    )
    url = reverse(f"admin:{operation}")
    target = (
        "apps.core.admin.tidy_media"
        if operation == "core_file_tidy_media"
        else "apps.projects.admin.relabel_project_files"
    )
    with patch(target, return_value=0) as run:
        assert client.post(url).status_code == 403
        run.assert_not_called()
        assert client.get(url).status_code == 200
        response = client.post(
            url, {"csrfmiddlewaretoken": client.cookies["csrftoken"].value}
        )
        assert response.status_code == 302
        run.assert_called_once_with()


def test_tidy_media_preserves_referenced_originals_thumbnails_and_gitkeep(
    settings: Settings, tmp_path: Path
) -> None:
    settings.MEDIA_ROOT = tmp_path
    for name in [
        "content/used.jpg",
        "thumbnail/used.jpg",
        "content/unused.jpg",
        "preview/old.jpg",
        ".gitkeep",
    ]:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"test")
    File.objects.create(content="content/used.jpg", thumbnail="thumbnail/used.jpg")
    assert tidy_media() == 2
    assert (tmp_path / "content/used.jpg").exists()
    assert (tmp_path / "thumbnail/used.jpg").exists()
    assert (tmp_path / ".gitkeep").exists()
    assert not (tmp_path / "content/unused.jpg").exists()
    assert not (tmp_path / "preview/old.jpg").exists()
    assert File.objects.count() == 1
    assert tidy_media() == 0


def test_orphan_files_exclude_post_files_and_covers() -> None:
    cover = File.objects.create(content="cover.jpg")
    main = File.objects.create(content="main.jpg")
    attachment = File.objects.create(content="attachment.jpg")
    orphan = File.objects.create(content="orphan.jpg")
    project = Project.objects.create(
        name="Private", link="private", cover=cover, is_public=False
    )
    post = Post.objects.create(project=project, number=0, is_draft=True, main_file=main)
    PostFile.objects.create(post=post, file=attachment)
    assert list(find_orphan_files()) == [orphan]
    assert File.objects.count() == 4


def test_relabel_all_projects_drafts_order_duplicates_and_shared_files(
    client: Client,
) -> None:
    cover = File.objects.create(content="cover.jpg", label="cover")
    main = File.objects.create(content="main.JPG", label="old")
    attachment = File.objects.create(content="second.png", label="old")
    shared = File.objects.create(content="shared.pdf", label="old")
    draft_file = File.objects.create(content="draft.gif", label="old")
    first = Project.objects.create(name="First", link="first", cover=cover)
    second = Project.objects.create(
        name="Second", link="second", cover=cover, is_public=False
    )
    draft = Post.objects.create(
        project=first, number=-2, is_draft=True, main_file=draft_file
    )
    post = Post.objects.create(project=first, number=7, main_file=main)
    PostFile.objects.create(post=post, file=attachment, order=1)
    PostFile.objects.create(post=post, file=main, order=2)
    PostFile.objects.create(post=post, file=shared, order=3)
    Post.objects.create(project=second, number=3, main_file=shared)
    client.force_login(
        get_user_model().objects.create_superuser("admin", password="test")
    )
    url = reverse("admin:projects_post_relabel_files")
    assert client.get(url).status_code == 200
    main.refresh_from_db()
    assert main.label == "old"
    response = client.post(url, follow=True)
    assert response.status_code == 200
    assert "Обновлено меток файлов: 4." in response.content.decode()
    expected = [
        (main, "first_7_1.jpg"),
        (attachment, "first_7_2.png"),
        (shared, "second_3_1.pdf"),
        (draft_file, "first_d2_1.gif"),
        (cover, "cover"),
    ]
    for file, label in expected:
        old_path = file.content.name
        file.refresh_from_db()
        assert file.label == label
        assert file.content.name == old_path
    assert relabel_project_files() == 0
    draft.refresh_from_db()
    assert draft.number == -2
