from django.urls import path

from .auth_views import csrf_token, login_view, logout_view, session

app_name = "core"

urlpatterns = [
    path("csrf/", csrf_token, name="csrf"),
    path("session/", session, name="session"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
