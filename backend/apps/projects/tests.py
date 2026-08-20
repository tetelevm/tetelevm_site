from datetime import date

from django import forms
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.core.models import File, FileType

from .admin import PostAdmin, PostAdminForm
from .models import Post, PostFile, PostListType, PostType, Project


class ProjectModelTests(TestCase):
    def setUp(self) -> None:
        self.cover = File.objects.create(content="cover.jpg")

    def test_projects_are_ordered_by_order(self) -> None:
        second = Project.objects.create(
            name="Second",
            link="second",
            cover=self.cover,
            post_type=PostType.TEXT,
            post_list_type=PostListType.TEXT,
            order=2,
        )
        first = Project.objects.create(
            name="First",
            link="first",
            cover=self.cover,
            post_type=PostType.TEXT,
            post_list_type=PostListType.TEXT,
            order=1,
        )

        self.assertEqual(list(Project.objects.all()), [first, second])

    def test_project_link_is_unique(self) -> None:
        Project.objects.create(
            name="First",
            link="same",
            cover=self.cover,
            post_type=PostType.TEXT,
            post_list_type=PostListType.TEXT,
        )

        with self.assertRaises(IntegrityError):
            Project.objects.create(
                name="Second",
                link="same",
                cover=self.cover,
                post_type=PostType.TEXT,
                post_list_type=PostListType.TEXT,
            )


class PostDisplayLabelTests(TestCase):
    def setUp(self) -> None:
        self.cover = File.objects.create(content="cover.jpg")
        self.project = Project.objects.create(
            name="Project",
            link="project",
            cover=self.cover,
        )

    def test_display_label_prefers_name_then_text(self) -> None:
        post = Post.objects.create(
            project=self.project,
            number=1,
            name="  A post name  ",
            text="Ignored text",
        )

        self.assertEqual(post.display_label, "A post name")

        post.name = ""
        post.text = "  A text\nexcerpt  "
        self.assertEqual(post.display_label, "A text excerpt")

    def test_display_label_truncates_long_text(self) -> None:
        post = Post.objects.create(
            project=self.project,
            number=1,
            text="word " * 40,
        )

        self.assertEqual(len(post.display_label), 90)
        self.assertTrue(post.display_label.endswith("..."))

    def test_annotated_file_labels_do_not_make_n_plus_one_queries(self) -> None:
        photo = File.objects.create(
            original_name="photo.jpg",
            file_type=FileType.PHOTO,
            content="content/photo.jpg",
        )
        audio = File.objects.create(
            original_name="audio.mp3",
            file_type=FileType.AUDIO,
            content="content/audio.mp3",
        )
        post_with_files = Post.objects.create(
            project=self.project,
            number=1,
            main_file=photo,
        )
        PostFile.objects.create(post=post_with_files, file=photo, order=0)
        PostFile.objects.create(post=post_with_files, file=audio, order=1)
        Post.objects.create(project=self.project, number=2)

        with self.assertNumQueries(1):
            labels = [
                post.display_label
                for post in Post.objects.with_display_file_counts().order_by(
                    "number"
                )
            ]

        self.assertEqual(labels, ["📷 1 · 🎵 1", "🌀"])

    def test_string_representation_uses_display_label(self) -> None:
        post = Post.objects.create(
            project=self.project,
            number=7,
            text="A text-only post",
        )

        self.assertEqual(str(post), "Project: #7 — A text-only post")


class PostAdminTests(TestCase):
    def setUp(self) -> None:
        self.cover = File.objects.create(content="cover.jpg")
        self.project = Project.objects.create(
            name="Project",
            link="project",
            cover=self.cover,
        )
        self.post = Post.objects.create(project=self.project, number=1)
        photo = File.objects.create(
            original_name="photo.jpg",
            file_type=FileType.PHOTO,
            content="content/photo.jpg",
            thumbnail="thumbnail/photo.jpg",
        )
        PostFile.objects.create(post=self.post, file=photo, order=0)
        user_model = get_user_model()
        self.admin = user_model.objects.create_superuser(
            "admin",
            password="admin",
        )

    def test_post_changelist_uses_display_label(self) -> None:
        self.client.force_login(self.admin)

        response = self.client.get(reverse("admin:projects_post_changelist"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "📷 1")

    def test_post_file_inline_displays_thumbnail(self) -> None:
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("admin:projects_post_change", args=(self.post.id,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/files/thumbnail/photo.jpg")
        self.assertContains(response, 'width="64"')

    def test_post_change_form_uses_typed_extra_fields_and_custom_layout(
        self,
    ) -> None:
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("admin:projects_post_change", args=(self.post.id,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'name="extra"')
        self.assertContains(response, 'name="extra_md"')
        self.assertContains(response, 'name="extra_original_title"')
        self.assertContains(response, 'name="extra_location_latitude"')
        self.assertContains(response, "data-project-post-types=")
        self.assertNotContains(response, "field-project field-number")
        self.assertNotContains(response, "field-name field-date")
        self.assertNotContains(response, "field-related_posts field-tags")
        self.assertContains(response, "projects/admin/post_form.css")
        self.assertContains(response, "projects/admin/post_extra.js")

    def test_post_change_form_loads_anime_extra_values(self) -> None:
        self.project.post_type = PostType.ANIME
        self.project.save(update_fields=("post_type",))
        self.post.extra = {
            "original_title": "Sousou no Frieren",
            "season": "Сезон 2",
            "rating": 9,
            "result": "да",
        }
        self.post.save(update_fields=("extra",))
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("admin:projects_post_change", args=(self.post.id,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="Sousou no Frieren"')
        self.assertContains(response, 'value="Сезон 2"')
        self.assertContains(response, 'value="9"')

    def test_related_post_autocomplete_searches_project_and_number(self) -> None:
        self.project.name = "Погулялки"
        self.project.save(update_fields=("name",))
        target = Post.objects.create(project=self.project, number=10)
        Post.objects.create(project=self.project, number=11)
        other_project = Project.objects.create(
            name="Другой проект",
            link="other-project",
            cover=self.cover,
        )
        Post.objects.create(project=other_project, number=10)
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("admin:autocomplete"),
            {
                "app_label": "projects",
                "model_name": "post",
                "field_name": "related_posts",
                "term": "погулялки #10",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [result["id"] for result in response.json()["results"]],
            [str(target.id)],
        )

    def test_post_admin_uses_typed_extra_fields(self) -> None:
        form = PostAdminForm(instance=self.post)

        self.assertNotIn("extra", form.fields)
        self.assertIsInstance(form.fields["extra_md"], forms.BooleanField)
        self.assertFalse(form.fields["extra_md"].required)
        self.assertFalse(form.fields["extra_md"].disabled)
        self.assertIsInstance(
            form.fields["extra_anime_rating"],
            forms.IntegerField,
        )
        self.assertIsInstance(
            form.fields["extra_abandoned_rating"],
            forms.FloatField,
        )
        self.assertTrue(form.fields["extra_anime_rating"].disabled)

    def test_anime_extra_fields_use_existing_values(self) -> None:
        self.project.post_type = PostType.ANIME
        self.project.save(update_fields=("post_type",))
        self.post.extra = {
            "original_title": "Sousou no Frieren",
            "season": "Сезон 2",
            "rating": 9,
            "result": "да",
        }
        self.post.save(update_fields=("extra",))

        form = PostAdminForm(instance=self.post)

        self.assertEqual(
            form.initial["extra_original_title"],
            "Sousou no Frieren",
        )
        self.assertEqual(form.initial["extra_season"], "Сезон 2")
        self.assertEqual(form.initial["extra_anime_rating"], 9)
        self.assertTrue(form.fields["extra_original_title"].required)
        self.assertFalse(form.fields["extra_season"].required)
        self.assertFalse(form.fields["extra_anime_rating"].disabled)
        self.assertEqual(form.fields["extra_anime_rating"].min_value, 1)
        self.assertEqual(form.fields["extra_anime_rating"].max_value, 10)

    def test_anime_rating_is_limited_to_ten(self) -> None:
        self.project.post_type = PostType.ANIME
        self.project.save(update_fields=("post_type",))

        form = PostAdminForm(
            data={
                "project": self.project.id,
                "number": self.post.number,
                "name": "",
                "text": "",
                "extra_original_title": "Title",
                "extra_anime_rating": 11,
                "extra_result": "да",
            },
            instance=self.post,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("extra_anime_rating", form.errors)

    def test_abandoned_extra_fields_are_serialized_and_preserve_unknowns(
        self,
    ) -> None:
        self.project.post_type = PostType.ABANDONED
        self.project.save(update_fields=("post_type",))
        self.post.extra = {
            "custom": {"kept": True},
            "original_title": "remove me",
            "location": {"note": "keep me", "link": "old"},
        }
        self.post.save(update_fields=("extra",))
        form = PostAdminForm(
            data={
                "project": self.project.id,
                "number": self.post.number,
                "name": "",
                "text": "",
                "extra_abandoned_rating": "4.5",
                "extra_location_latitude": "41.6880746",
                "extra_location_longitude": "44.8216462",
                "extra_location_link": "osm.link/qwerty",
                "extra_uniqueness": 5,
                "extra_monumentality": 3,
                "extra_atmosphere": 4,
                "extra_liveliness": 2,
            },
            instance=self.post,
        )

        self.assertTrue(form.is_valid(), form.errors)
        post = form.save()

        self.assertEqual(post.extra["rating"], 4.5)
        self.assertEqual(post.extra["location"]["latitude"], 41.6880746)
        self.assertEqual(post.extra["location"]["longitude"], 44.8216462)
        self.assertEqual(post.extra["location"]["link"], "osm.link/qwerty")
        self.assertEqual(post.extra["location"]["note"], "keep me")
        self.assertEqual(post.extra["custom"], {"kept": True})
        self.assertNotIn("original_title", post.extra)

    def test_abandoned_integer_scores_are_limited_to_five(self) -> None:
        self.project.post_type = PostType.ABANDONED
        self.project.save(update_fields=("post_type",))
        form = PostAdminForm(
            data={
                "project": self.project.id,
                "number": self.post.number,
                "name": "",
                "text": "",
                "extra_abandoned_rating": "4.5",
                "extra_location_latitude": "41.6",
                "extra_location_longitude": "44.8",
                "extra_location_link": "osm.link/qwerty",
                "extra_uniqueness": 6,
                "extra_monumentality": 3,
                "extra_atmosphere": 4,
                "extra_liveliness": 2,
            },
            instance=self.post,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("extra_uniqueness", form.errors)

    def test_post_admin_field_layout(self) -> None:
        self.assertEqual(
            PostAdmin.fieldsets[0][1]["fields"],
            (
                "project",
                "number",
                "name",
                "date",
                "main_file",
                "text",
            ),
        )
        self.assertIn(
            "fieldset-extra",
            PostAdmin.fieldsets[1][1]["classes"],
        )
        self.assertEqual(
            PostAdmin.fieldsets[1][1]["fields"],
            (
                "extra_md",
                "extra_original_title",
                "extra_season",
                "extra_anime_rating",
                "extra_result",
                "extra_abandoned_rating",
                "extra_location_link",
                "extra_location_latitude",
                "extra_location_longitude",
                "extra_uniqueness",
                "extra_monumentality",
                "extra_atmosphere",
                "extra_liveliness",
            ),
        )
        self.assertEqual(
            PostAdmin.fieldsets[2][1]["fields"],
            (
                "related_posts",
                "tags",
            ),
        )


class ProjectApiTests(APITestCase):
    def setUp(self) -> None:
        self.cover = File.objects.create(content="cover.jpg")
        self.public_project = Project.objects.create(
            name="Public",
            description="A short project description.",
            link="public",
            cover=self.cover,
            post_type=PostType.TEXT,
            post_list_type=PostListType.TRAVEL,
            is_public=True,
        )
        self.private_project = Project.objects.create(
            name="Private",
            link="private",
            cover=self.cover,
            post_type=PostType.PHOTO,
            post_list_type=PostListType.PHOTO,
            is_public=False,
        )
        self.public_post = Post.objects.create(
            project=self.public_project,
            number=1,
            date=date(2026, 8, 17),
            name="Public post",
            extra={"rating": 8},
        )
        self.private_post = Post.objects.create(
            project=self.private_project,
            number=1,
            name="Private post",
        )
        user_model = get_user_model()
        self.guest = user_model.objects.create_user("guest", password="guest")
        self.admin = user_model.objects.create_superuser(
            "admin",
            password="admin",
        )

    def test_anonymous_user_only_sees_public_projects(self) -> None:
        response = self.client.get(reverse("projects:project-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual([project["link"] for project in response.data], ["public"])

    def test_project_list_includes_post_count(self) -> None:
        Post.objects.create(
            project=self.public_project,
            number=2,
            name="Another public post",
        )

        response = self.client.get(reverse("projects:project-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["postCount"], 2)

    def test_project_list_uses_explicit_order_then_id(self) -> None:
        self.public_project.order = 2
        self.public_project.save(update_fields=("order",))
        Project.objects.create(
            name="First",
            link="first",
            cover=self.cover,
            order=1,
        )
        Project.objects.create(
            name="Same order, later id",
            link="same-order",
            cover=self.cover,
            order=2,
        )

        response = self.client.get(reverse("projects:project-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [project["link"] for project in response.data],
            ["first", "public", "same-order"],
        )

    def test_anonymous_user_can_retrieve_public_project_posts(self) -> None:
        response = self.client.get(
            reverse(
                "projects:project-posts",
                kwargs={"project_code": "public"},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["postCount"], 1)
        self.assertEqual(response.data["postListType"], PostListType.TRAVEL)
        self.assertEqual(response.data["posts"][0]["rating"], 8)
        self.assertEqual(response.data["posts"][0]["label"], "Public post")
        self.assertEqual(response.data["posts"][0]["date"], "2026-08-17")
        self.assertNotIn("extra", response.data["posts"][0])
        self.assertNotIn("files", response.data["posts"][0])
        self.assertNotIn("tags", response.data["posts"][0])
        self.assertEqual(
            response.data["description"],
            "A short project description.",
        )
        self.assertEqual([post["number"] for post in response.data["posts"]], [1])
        self.assertEqual(
            response.data["pagination"],
            {
                "page": 1,
                "pageSize": 50,
                "totalPages": 1,
                "totalItems": 1,
            },
        )

    def test_project_posts_are_paginated_by_fifty(self) -> None:
        Post.objects.bulk_create(
            [
                Post(project=self.public_project, number=number)
                for number in range(2, 52)
            ]
        )

        first_page = self.client.get(
            reverse(
                "projects:project-posts",
                kwargs={"project_code": "public"},
            )
        )
        response = self.client.get(
            reverse(
                "projects:project-posts",
                kwargs={"project_code": "public"},
            ),
            {"page": 2},
        )

        self.assertEqual(first_page.status_code, 200)
        self.assertEqual(first_page.data["posts"][0]["number"], 51)
        self.assertEqual(first_page.data["posts"][-1]["number"], 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([post["number"] for post in response.data["posts"]], [1])
        self.assertEqual(response.data["pagination"]["page"], 2)
        self.assertEqual(response.data["pagination"]["totalPages"], 2)
        self.assertEqual(response.data["pagination"]["totalItems"], 51)

    def test_general_post_list_uses_text_excerpt_when_name_is_missing(self) -> None:
        self.public_project.post_list_type = PostListType.POST
        self.public_project.save(update_fields=("post_list_type",))
        self.public_post.name = ""
        self.public_post.text = "  A text\nexcerpt  "
        self.public_post.save(update_fields=("name", "text"))

        response = self.client.get(
            reverse(
                "projects:project-posts",
                kwargs={"project_code": "public"},
            )
        )

        self.assertEqual(response.data["posts"][0]["label"], "A text excerpt")

    def test_every_post_list_type_uses_shared_label(self) -> None:
        self.public_post.name = ""
        self.public_post.text = "  A shared\nlabel  "
        self.public_post.save(update_fields=("name", "text"))

        for post_list_type in PostListType:
            with self.subTest(post_list_type=post_list_type):
                self.public_project.post_list_type = post_list_type
                self.public_project.save(update_fields=("post_list_type",))

                response = self.client.get(
                    reverse(
                        "projects:project-posts",
                        kwargs={"project_code": "public"},
                    )
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data["posts"][0]["label"], "A shared label")

    def test_general_post_list_summarizes_files_and_uses_first_photo(self) -> None:
        self.public_project.post_list_type = PostListType.POST
        self.public_project.save(update_fields=("post_list_type",))
        self.public_post.name = ""
        self.public_post.text = ""
        self.public_post.save(update_fields=("name", "text"))
        photo = File.objects.create(
            original_name="photo.jpg",
            file_type=FileType.PHOTO,
            content="content/photo.jpg",
            thumbnail="thumbnail/photo.jpg",
        )
        audio = File.objects.create(
            original_name="song.mp3",
            file_type=FileType.AUDIO,
            content="content/song.mp3",
        )
        PostFile.objects.create(post=self.public_post, file=photo, order=0)
        PostFile.objects.create(post=self.public_post, file=audio, order=1)

        response = self.client.get(
            reverse(
                "projects:project-posts",
                kwargs={"project_code": "public"},
            )
        )

        summary = response.data["posts"][0]
        self.assertEqual(summary["label"], "📷 1 · 🎵 1")
        self.assertEqual(summary["thumbnail"], "/files/thumbnail/photo.jpg")

    def test_plasticine_list_uses_preview_instead_of_thumbnail(self) -> None:
        self.public_project.post_list_type = PostListType.PLASTICINE
        self.public_project.save(update_fields=("post_list_type",))
        photo = File.objects.create(
            original_name="plasticine.jpg",
            file_type=FileType.PHOTO,
            content="content/plasticine.jpg",
            preview="preview/plasticine.jpg",
            thumbnail="thumbnail/plasticine.jpg",
        )
        self.public_post.main_file = photo
        self.public_post.save(update_fields=("main_file",))

        response = self.client.get(
            reverse(
                "projects:project-posts",
                kwargs={"project_code": "public"},
            )
        )

        self.assertEqual(
            response.data["posts"][0]["mainFile"]["link"],
            "/files/preview/plasticine.jpg",
        )

    def test_anonymous_user_cannot_retrieve_private_project_posts(self) -> None:
        response = self.client.get(
            reverse(
                "projects:project-posts",
                kwargs={"project_code": "private"},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_project_post_list_returns_null_for_missing_rating(self) -> None:
        self.public_post.extra = {}
        self.public_post.save(update_fields=("extra",))

        response = self.client.get(
            reverse(
                "projects:project-posts",
                kwargs={"project_code": "public"},
            )
        )

        self.assertIsNone(response.data["posts"][0]["rating"])
        self.assertEqual(response.data["posts"][0]["date"], "2026-08-17")

    def test_anonymous_user_can_retrieve_public_post(self) -> None:
        response = self.client.get(
            reverse(
                "projects:post-detail",
                kwargs={"project_code": "public", "post_num": 1},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Public post")
        self.assertEqual(response.data["projectCode"], "public")
        self.assertEqual(response.data["projectName"], "Public")
        self.assertEqual(response.data["postType"], PostType.TEXT)
        self.assertEqual(response.data["link"], "/archive/public/1/")
        self.assertEqual(response.data["relatedPosts"], [])
        self.assertNotIn("relatedPost", response.data)
        self.assertIsNone(response.data["previousPost"])
        self.assertIsNone(response.data["nextPost"])

    def test_post_detail_includes_nearest_adjacent_posts(self) -> None:
        previous_post = Post.objects.create(
            project=self.public_project,
            number=4,
            name="Earlier post",
        )
        current_post = Post.objects.create(
            project=self.public_project,
            number=10,
            name="Current post",
        )
        next_post = Post.objects.create(
            project=self.public_project,
            number=14,
            text="Later post without a name",
        )
        Post.objects.create(
            project=self.public_project,
            number=20,
            name="Farther post",
        )

        response = self.client.get(
            reverse(
                "projects:post-detail",
                kwargs={"project_code": "public", "post_num": 10},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["previousPost"],
            {
                "number": previous_post.number,
                "link": "/archive/public/4/",
                "label": "Earlier post",
            },
        )
        self.assertEqual(
            response.data["nextPost"],
            {
                "number": next_post.number,
                "link": "/archive/public/14/",
                "label": "Later post without a name",
            },
        )
        self.assertEqual(response.data["number"], current_post.number)

    def test_post_detail_adjacent_navigation_has_project_boundaries(self) -> None:
        last_post = Post.objects.create(
            project=self.public_project,
            number=3,
            name="Last post",
        )

        first_response = self.client.get(
            reverse(
                "projects:post-detail",
                kwargs={"project_code": "public", "post_num": 1},
            )
        )
        last_response = self.client.get(
            reverse(
                "projects:post-detail",
                kwargs={"project_code": "public", "post_num": 3},
            )
        )

        self.assertIsNone(first_response.data["previousPost"])
        self.assertEqual(first_response.data["nextPost"]["number"], 3)
        self.assertEqual(last_response.data["previousPost"]["number"], 1)
        self.assertIsNone(last_response.data["nextPost"])
        self.assertEqual(last_response.data["number"], last_post.number)

    def test_related_posts_are_symmetric_and_use_row_summaries(self) -> None:
        photo = File.objects.create(
            original_name="related.jpg",
            file_type=FileType.PHOTO,
            content="content/related.jpg",
            thumbnail="thumbnail/related.jpg",
        )
        related_post = Post.objects.create(
            project=self.public_project,
            number=2,
            date=date(2026, 8, 18),
            name="Related post",
            main_file=photo,
        )
        self.public_post.related_posts.add(related_post)

        response = self.client.get(
            reverse(
                "projects:post-detail",
                kwargs={"project_code": "public", "post_num": 1},
            )
        )

        self.assertEqual(
            response.data["relatedPosts"],
            [
                {
                    "id": related_post.id,
                    "number": 2,
                    "link": "/archive/public/2/",
                    "label": "Related post",
                    "thumbnail": "/files/thumbnail/related.jpg",
                    "date": "2026-08-18",
                }
            ],
        )

        reverse_response = self.client.get(
            reverse(
                "projects:post-detail",
                kwargs={"project_code": "public", "post_num": 2},
            )
        )

        self.assertEqual(
            [post["link"] for post in reverse_response.data["relatedPosts"]],
            ["/archive/public/1/"],
        )

    def test_anonymous_user_does_not_receive_private_related_posts(self) -> None:
        self.public_post.related_posts.add(self.private_post)

        response = self.client.get(
            reverse(
                "projects:post-detail",
                kwargs={"project_code": "public", "post_num": 1},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["relatedPosts"], [])

    def test_guest_receives_private_related_posts(self) -> None:
        self.public_post.related_posts.add(self.private_post)
        self.client.force_login(self.guest)

        response = self.client.get(
            reverse(
                "projects:post-detail",
                kwargs={"project_code": "public", "post_num": 1},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [post["link"] for post in response.data["relatedPosts"]],
            ["/archive/private/1/"],
        )

    def test_anonymous_user_cannot_retrieve_post_from_private_project(self) -> None:
        response = self.client.get(
            reverse(
                "projects:post-detail",
                kwargs={"project_code": "private", "post_num": 1},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_guest_can_retrieve_private_project_posts(self) -> None:
        self.client.force_login(self.guest)

        response = self.client.get(
            reverse(
                "projects:project-posts",
                kwargs={"project_code": "private"},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["postListType"], PostListType.PHOTO)

    def test_guest_cannot_write_projects(self) -> None:
        self.client.force_login(self.guest)

        response = self.client.post(
            reverse("projects:project-list"),
            {"name": "Guest project"},
        )

        self.assertEqual(response.status_code, 405)

    def test_guest_can_retrieve_post_from_private_project(self) -> None:
        self.client.force_login(self.guest)

        response = self.client.get(
            reverse(
                "projects:post-detail",
                kwargs={"project_code": "private", "post_num": 1},
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_admin_can_retrieve_private_project_posts(self) -> None:
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse(
                "projects:project-posts",
                kwargs={"project_code": "private"},
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_admin_can_retrieve_post_from_private_project(self) -> None:
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse(
                "projects:post-detail",
                kwargs={"project_code": "private", "post_num": 1},
            )
        )

        self.assertEqual(response.status_code, 200)
