from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.core.models import File

from .models import Post, PostListType, PostType, Project


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

    def test_anonymous_user_can_retrieve_public_project_posts(self) -> None:
        response = self.client.get(
            reverse(
                "projects:project-posts",
                kwargs={"project_code": "public"},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["postListType"], PostListType.TRAVEL)
        self.assertEqual(response.data["posts"][0]["rating"], 8)
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

        response = self.client.get(
            reverse(
                "projects:project-posts",
                kwargs={"project_code": "public"},
            ),
            {"page": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual([post["number"] for post in response.data["posts"]], [51])
        self.assertEqual(response.data["pagination"]["page"], 2)
        self.assertEqual(response.data["pagination"]["totalPages"], 2)
        self.assertEqual(response.data["pagination"]["totalItems"], 51)

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
        self.assertEqual(response.data["link"], "/projects/public/1/")

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
