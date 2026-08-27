from __future__ import annotations

from django.db.models import Count, Prefetch, QuerySet
from django.db.models.fields.json import KeyTransform
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Project, Tag
from .serializers import (
    PostListSerializer,
    PostSerializer,
    ProjectListSerializer,
)

RANDOM_POST_TAG_CODE = "star"


def visible_projects(user_is_authenticated: bool) -> QuerySet[Project]:
    projects = Project.objects.select_related("cover")
    if user_is_authenticated:
        return projects
    return projects.filter(is_public=True)


def with_post_count(projects: QuerySet[Project]) -> QuerySet[Project]:
    return projects.annotate(
        post_count=Count("posts", distinct=True)
    ).order_by("order", "id")


class ProjectListView(ListAPIView):
    serializer_class = ProjectListSerializer

    def get_queryset(self) -> QuerySet[Project]:
        return with_post_count(
            visible_projects(self.request.user.is_authenticated)
        )


class RandomPostView(APIView):
    def get(self, request: Request) -> Response:
        post = (
            Post.objects.filter(
                project__in=visible_projects(request.user.is_authenticated),
                tags__code=RANDOM_POST_TAG_CODE,
            )
            .select_related("project")
            .order_by("?")
            .first()
        )
        if post is None:
            return Response(
                {"detail": "No visible featured posts"},
                status=404,
            )
        return Response({"link": post.link})


class ProjectPostPagination(PageNumberPagination):
    page_size = 48
    page_query_param = "page"


class ProjectPostsView(RetrieveAPIView):
    serializer_class = ProjectListSerializer
    pagination_class = ProjectPostPagination
    lookup_field = "link"
    lookup_url_kwarg = "project_code"

    def get_queryset(self) -> QuerySet[Project]:
        return with_post_count(
            visible_projects(self.request.user.is_authenticated)
        )

    def retrieve(
        self,
        request: Request,
        *args: object,
        **kwargs: object,
    ) -> Response:
        project = self.get_object()
        posts = (
            project.posts.with_display_file_counts()
            .with_card_file()
            .select_related("project")
            .annotate(rating=KeyTransform("rating", "extra"))
            .defer("extra")
            .order_by("-number", "-id")
        )
        tag_code = request.query_params.get("tag", "").strip()
        if tag_code:
            posts = posts.filter(tags__code=tag_code)
        page = self.paginate_queryset(posts)
        assert page is not None
        assert self.paginator is not None

        data = dict(self.get_serializer(project).data)
        data["activeTag"] = None
        if tag_code:
            tag_name = (
                Tag.objects.filter(code=tag_code)
                .values_list("name", flat=True)
                .first()
            )
            data["activeTag"] = {
                "code": tag_code,
                "name": tag_name or tag_code,
            }
        data["posts"] = PostListSerializer(
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
        user_is_authenticated = self.request.user.is_authenticated
        related_posts = (
            Post.objects.filter(
                project__in=visible_projects(user_is_authenticated)
            )
            .with_display_file_counts()
            .select_related("project", "main_file")
            .prefetch_related("post_files__file")
            .defer("extra")
            .order_by("project__order", "project_id", "-number", "-id")
        )
        posts = Post.objects.filter(
            project__in=visible_projects(user_is_authenticated),
            project__link=self.kwargs["project_code"],
        ).with_adjacent_post_ids()
        return posts.select_related("project", "main_file").prefetch_related(
            "post_files__file",
            "tags",
            Prefetch("related_posts", queryset=related_posts),
        )

    def retrieve(
        self,
        request: Request,
        *args: object,
        **kwargs: object,
    ) -> Response:
        post = self.get_object()
        adjacent_ids = {
            post_id
            for post_id in (post.previous_post_id, post.next_post_id)
            if post_id is not None
        }
        adjacent_posts = {
            adjacent_post.id: adjacent_post
            for adjacent_post in (
                Post.objects.filter(id__in=adjacent_ids)
                .with_display_file_counts()
                .select_related("project", "main_file")
            )
        }
        post.previous_post_summary = adjacent_posts.get(post.previous_post_id)
        post.next_post_summary = adjacent_posts.get(post.next_post_id)
        return Response(self.get_serializer(post).data)
