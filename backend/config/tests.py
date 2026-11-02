from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.core.models import File
from apps.projects.models import Post, Project


class SearchDiscoveryTests(TestCase):
    def setUp(self) -> None:
        cover = File.objects.create(content="cover.jpg")
        self.public_project = Project.objects.create(
            name="Public",
            link="public-project",
            cover=cover,
            is_public=True,
        )
        self.private_project = Project.objects.create(
            name="Private",
            link="private-project",
            cover=cover,
            is_public=False,
        )

    def test_sitemap_contains_only_public_project_pages(self) -> None:
        response = self.client.get(reverse("sitemap"))
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "http://testserver/")
        self.assertContains(response, "http://testserver/archive/")
        self.assertContains(
            response,
            "http://testserver/archive/public-project/",
        )
        self.assertNotIn("private-project", content)

    def test_page_meta_does_not_expose_draft_posts(self) -> None:
        Post.objects.create(
            project=self.public_project,
            number=-1,
            name="Secret draft title",
            is_draft=True,
        )

        response = self.client.get(
            reverse("page-meta"),
            {"path": "/archive/public-project/-1/"},
        )

        self.assertNotContains(response, "Secret draft title")
        self.assertContains(response, "{{httpError 404}}")

    def test_page_meta_exposes_draft_to_staff_as_noindex(self) -> None:
        Post.objects.create(
            project=self.public_project,
            number=-1,
            name="Staff draft title",
            is_draft=True,
        )
        admin = get_user_model().objects.create_superuser(
            "admin",
            password="admin",
        )
        self.client.force_login(admin)

        response = self.client.get(
            reverse("page-meta"),
            {"path": "/archive/public-project/-1/"},
        )

        self.assertContains(response, "Staff draft title")
        self.assertContains(response, 'name="robots" content="noindex"')
        self.assertNotContains(response, "{{httpError 404}}")

    def test_page_meta_does_not_expose_private_project_to_anonymous_user(self) -> None:
        response = self.client.get(
            reverse("page-meta"),
            {"path": "/archive/private-project/"},
        )

        self.assertNotContains(response, "Private")

    def test_missing_page_meta_triggers_caddy_404_and_noindex(self) -> None:
        response = self.client.get(
            reverse("page-meta"),
            {"path": "/does-not-exist/"},
        )

        self.assertContains(response, 'name="robots" content="noindex"')
        self.assertContains(response, "{{httpError 404}}")
