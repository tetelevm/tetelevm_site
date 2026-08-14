from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.core.models import File

from .models import PostListType, PostType, Project


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

    def test_anonymous_user_cannot_retrieve_private_project(self) -> None:
        response = self.client.get(
            reverse("projects:project-detail", kwargs={"link": "private"})
        )

        self.assertEqual(response.status_code, 404)

    def test_guest_can_retrieve_private_project(self) -> None:
        self.client.force_login(self.guest)

        response = self.client.get(
            reverse("projects:project-detail", kwargs={"link": "private"})
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

    def test_admin_can_retrieve_private_project(self) -> None:
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("projects:project-detail", kwargs={"link": "private"})
        )

        self.assertEqual(response.status_code, 200)
