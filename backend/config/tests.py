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
        self.assertContains(response, "User-agent: TelegramBot\nAllow: /")
        self.assertNotContains(response, "Disallow: /login/")
        self.assertNotContains(response, "Disallow: /archive/random/")
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

    def test_formats_page_meta_describes_the_formats_archive(self) -> None:
        response = self.client.get(
            reverse("page-meta"),
            {"path": "/archive/"},
        )

        description = (
            "Архив форматов: тексты, фотографии и другое."
        )
        self.assertContains(
            response,
            f'<meta property="og:description" content="{description}" '
            "data-page-meta>",
            html=True,
        )
        self.assertContains(
            response,
            f'<meta name="description" content="{description}" '
            "data-page-meta>",
            html=True,
        )

    def test_legacy_formats_meta_uses_archive_canonical_url(self) -> None:
        response = self.client.get(
            reverse("page-meta"),
            {"path": "/formats/public-project/"},
        )

        self.assertContains(
            response,
            'rel="canonical" href="http://testserver/archive/public-project/"',
        )

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

    def test_missing_page_meta_triggers_caddy_404_and_noindex(self) -> None:
        response = self.client.get(
            reverse("page-meta"),
            {"path": "/does-not-exist/"},
        )

        self.assertContains(response, 'name="robots" content="noindex"')
        self.assertContains(response, "{{httpError 404}}")

    def test_login_meta_is_noindex_without_triggering_404(self) -> None:
        response = self.client.get(
            reverse("page-meta"),
            {"path": "/login/"},
        )

        self.assertContains(response, 'name="robots" content="noindex"')
        self.assertNotContains(response, "{{httpError 404}}")
