from __future__ import annotations

from django.db.models import QuerySet
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Project
from .serializers import ProjectDetailSerializer, ProjectListSerializer


def visible_projects(user_is_authenticated: bool) -> QuerySet[Project]:
    projects = Project.objects.select_related("cover")
    if user_is_authenticated:
        return projects
    return projects.filter(is_public=True)


class ProjectListView(ListAPIView):
    serializer_class = ProjectListSerializer

    def get_queryset(self) -> QuerySet[Project]:
        return visible_projects(self.request.user.is_authenticated)


class ProjectDetailView(RetrieveAPIView):
    serializer_class = ProjectDetailSerializer
    lookup_field = "link"

    def get_queryset(self) -> QuerySet[Project]:
        return visible_projects(self.request.user.is_authenticated).prefetch_related(
            "posts"
        )
