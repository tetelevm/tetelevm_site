from django.urls import path, register_converter

from .views import (
    FileDetailAdminView,
    PostDetailView,
    ProjectListView,
    ProjectPostTagsAdminView,
    ProjectPostsView,
    RandomPostView,
    TagListAdminView,
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
    path("tags/", TagListAdminView.as_view(), name="tag-list-admin"),
    path(
        "files/<uuid:file_id>/",
        FileDetailAdminView.as_view(),
        name="file-detail-admin",
    ),
    path("random-post/", RandomPostView.as_view(), name="random-post"),
    path(
        "formats/<str:project_code>/post-tags/",
        ProjectPostTagsAdminView.as_view(),
        name="project-post-tags-admin",
    ),
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
