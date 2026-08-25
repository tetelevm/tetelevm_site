from __future__ import annotations

from django.contrib.sitemaps import Sitemap
from django.db.models import QuerySet

from apps.projects.models import Project


class StaticSitemap(Sitemap):
    def items(self) -> tuple[str, str]:
        return ("/", "/archive/")

    def location(self, item: str) -> str:
        return item


class PublicProjectSitemap(Sitemap):
    def items(self) -> QuerySet[Project]:
        return Project.objects.filter(is_public=True).order_by("order", "id")

    def location(self, project: Project) -> str:
        return f"/archive/{project.link}/"


sitemaps: dict[str, Sitemap] = {
    "static": StaticSitemap(),
    "projects": PublicProjectSitemap(),
}
