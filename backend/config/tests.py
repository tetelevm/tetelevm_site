from __future__ import annotations

from django.test import TestCase
from django.urls import reverse

from apps.core.models import File, FileType
from apps.projects.models import Post, PostFile, Project


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

    def test_robots_txt_identifies_blocked_routes_and_sitemap(self) -> None:
        response = self.client.get(reverse("robots-txt"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertContains(response, "Disallow: /_admin/")
        self.assertContains(response, "Disallow: /_api/")
        self.assertContains(
            response,
            "Sitemap: http://testserver/sitemap.xml",
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

    def test_page_meta_uses_project_name_description_and_cover(self) -> None:
        self.public_project.description = "  Project\n description  "
        self.public_project.cover.preview = "preview/cover.jpg"
        self.public_project.cover.save(update_fields=("preview",))
        self.public_project.save(update_fields=("description",))

        response = self.client.get(
            reverse("page-meta"),
            {"path": "/archive/public-project/"},
        )

        self.assertContains(response, "<title data-page-meta>Public</title>")
        self.assertContains(response, 'content="tetelevm - Public"')
        self.assertContains(response, 'content="Project description"')
        self.assertContains(
            response,
            'content="http://testserver/files/preview/cover.jpg"',
        )

    def test_page_meta_uses_post_fallback_title_and_file_counts(self) -> None:
        photo = File.objects.create(
            content="content/photo.jpg",
            preview="preview/photo.jpg",
            file_type=FileType.PHOTO,
        )
        post = Post.objects.create(
            project=self.public_project,
            number=12,
            main_file=photo,
        )
        video = File.objects.create(
            content="content/video.mp4",
            file_type=FileType.VIDEO,
        )
        PostFile.objects.create(post=post, file=video, order=1)

        response = self.client.get(
            reverse("page-meta"),
            {"path": "/archive/public-project/12/"},
        )

        self.assertContains(
            response,
            "<title data-page-meta>Public #12</title>",
        )
        self.assertContains(response, 'content="tetelevm - Public - #12"')
        self.assertContains(response, 'content="1 📷 · 1 🎬"')
        self.assertContains(
            response,
            'content="http://testserver/files/preview/photo.jpg"',
        )

    def test_page_meta_does_not_expose_private_project_to_anonymous_user(self) -> None:
        response = self.client.get(
            reverse("page-meta"),
            {"path": "/archive/private-project/"},
        )

        self.assertNotContains(response, "Private")
