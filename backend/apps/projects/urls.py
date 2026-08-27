from django.urls import path

from .views import (
    PostDetailView,
    ProjectListView,
    ProjectPostsView,
    RandomPostView,
)

app_name = "projects"

urlpatterns = [
    path("random-post/", RandomPostView.as_view(), name="random-post"),
    path("formats/", ProjectListView.as_view(), name="project-list"),
    path(
        "formats/<str:project_code>/",
        ProjectPostsView.as_view(),
        name="project-posts",
    ),
    path(
        "formats/<str:project_code>/<int:post_num>/",
        PostDetailView.as_view(),
        name="post-detail",
    ),
    path("projects/", ProjectListView.as_view()),
    path(
        "projects/<str:project_code>/",
        ProjectPostsView.as_view(),
    ),
    path(
        "projects/<str:project_code>/<int:post_num>/",
        PostDetailView.as_view(),
    ),
]
