from django.urls import path

from .views import PostDetailView, ProjectListView, ProjectPostsView

app_name = "projects"

urlpatterns = [
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path(
        "projects/<str:project_code>/",
        ProjectPostsView.as_view(),
        name="project-posts",
    ),
    path(
        "projects/<str:project_code>/<int:post_num>/",
        PostDetailView.as_view(),
        name="post-detail",
    ),
]
