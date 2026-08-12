from django.db import IntegrityError
from django.test import TestCase

from apps.core.models import File

from .models import ContentType, Project


class ProjectModelTests(TestCase):
    def setUp(self) -> None:
        self.cover = File.objects.create(content="cover.jpg")
        self.content_type = ContentType.objects.create(
            name="Articles",
            code="articles",
        )

    def test_projects_are_ordered_by_order(self) -> None:
        second = Project.objects.create(
            name="Second",
            link="second",
            cover=self.cover,
            content_type=self.content_type,
            order=2,
        )
        first = Project.objects.create(
            name="First",
            link="first",
            cover=self.cover,
            content_type=self.content_type,
            order=1,
        )

        self.assertEqual(list(Project.objects.all()), [first, second])

    def test_project_link_is_unique(self) -> None:
        Project.objects.create(
            name="First",
            link="same",
            cover=self.cover,
            content_type=self.content_type,
        )

        with self.assertRaises(IntegrityError):
            Project.objects.create(
                name="Second",
                link="same",
                cover=self.cover,
                content_type=self.content_type,
            )
