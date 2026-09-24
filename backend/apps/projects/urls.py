from django.urls import path, register_converter

from .views import (
    PostDetailView,
    ProjectListView,
    ProjectPostsView,
    RandomPostView,
)

app_name = "projects"


class SignedIntConverter:
    regex = r"-?[0-9]+"

    def to_python(self, value: str) -> int:
        return int(value)

    def to_url(self, value: int) -> str:
        return str(value)


register_converter(SignedIntConverter, "signed_int")

urlpatterns = [
    path("random-post/", RandomPostView.as_view(), name="random-post"),
    path("formats/", ProjectListView.as_view(), name="project-list"),
    path(
        "formats/<str:project_code>/",
        ProjectPostsView.as_view(),
        name="project-posts",
    ),
    path(
        "formats/<str:project_code>/<signed_int:post_num>/",
        PostDetailView.as_view(),
        name="post-detail",
    ),
    path("projects/", ProjectListView.as_view()),
    path(
        "projects/<str:project_code>/",
        ProjectPostsView.as_view(),
    ),
    path(
        "projects/<str:project_code>/<signed_int:post_num>/",
        PostDetailView.as_view(),
    ),
]
