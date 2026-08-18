from __future__ import annotations

from django.db.models import QuerySet
from django.db.models.fields.json import KeyTransform
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Post, PostListType, Project
from .serializers import (
    GeneralPostListSerializer,
    PostListSerializer,
    PostSerializer,
    ProjectListSerializer,
)


def visible_projects(user_is_authenticated: bool) -> QuerySet[Project]:
    projects = Project.objects.select_related("cover")
    if user_is_authenticated:
        return projects
    return projects.filter(is_public=True)


class ProjectListView(ListAPIView):
    serializer_class = ProjectListSerializer

    def get_queryset(self) -> QuerySet[Project]:
        return visible_projects(self.request.user.is_authenticated)


class ProjectPostPagination(PageNumberPagination):
    page_size = 50
    page_query_param = "page"


class ProjectPostsView(RetrieveAPIView):
    serializer_class = ProjectListSerializer
    pagination_class = ProjectPostPagination
    lookup_field = "link"
    lookup_url_kwarg = "project_code"

    def get_queryset(self) -> QuerySet[Project]:
        return visible_projects(self.request.user.is_authenticated)

    def retrieve(
        self,
        request: Request,
        *args: object,
        **kwargs: object,
    ) -> Response:
        project = self.get_object()
        posts = (
            project.posts.select_related("project", "main_file")
            .annotate(rating=KeyTransform("rating", "extra"))
            .defer("extra")
            .order_by("-number", "-id")
        )
        list_serializer = PostListSerializer
        if project.post_list_type == PostListType.POST:
            posts = posts.prefetch_related("post_files__file")
            list_serializer = GeneralPostListSerializer
        page = self.paginate_queryset(posts)
        assert page is not None
        assert self.paginator is not None

        data = dict(self.get_serializer(project).data)
        data["posts"] = list_serializer(
            page,
            many=True,
            context=self.get_serializer_context(),
        ).data
        data["pagination"] = {
            "page": self.paginator.page.number,
            "pageSize": self.paginator.page_size,
            "totalPages": self.paginator.page.paginator.num_pages,
            "totalItems": self.paginator.page.paginator.count,
        }
        return Response(data)


class PostDetailView(RetrieveAPIView):
    serializer_class = PostSerializer
    lookup_field = "number"
    lookup_url_kwarg = "post_num"

    def get_queryset(self) -> QuerySet[Post]:
        posts = Post.objects.filter(
            project__in=visible_projects(self.request.user.is_authenticated),
            project__link=self.kwargs["project_code"],
        )
        return posts.select_related(
            "project",
            "main_file",
            "related_post",
        ).prefetch_related("post_files__file", "tags")
