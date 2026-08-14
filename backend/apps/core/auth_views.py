from __future__ import annotations

import json
from json import JSONDecodeError

from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST


@ensure_csrf_cookie
@require_GET
def csrf_token(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"csrfToken": get_token(request)})


@require_GET
def session(request: HttpRequest) -> JsonResponse:
    user = request.user
    return JsonResponse(
        {
            "isAuthenticated": user.is_authenticated,
            "username": user.get_username() if user.is_authenticated else None,
            "isStaff": user.is_staff if user.is_authenticated else False,
        }
    )


@csrf_protect
@require_POST
def login_view(request: HttpRequest) -> JsonResponse:
    try:
        credentials = json.loads(request.body)
    except (JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"detail": "Invalid request body"}, status=400)
    if not isinstance(credentials, dict):
        return JsonResponse({"detail": "Invalid request body"}, status=400)

    username = credentials.get("username")
    password = credentials.get("password")
    if not isinstance(username, str) or not isinstance(password, str):
        return JsonResponse({"detail": "Username and password are required"}, status=400)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"detail": "Invalid credentials"}, status=401)

    login(request, user)
    return JsonResponse(
        {
            "isAuthenticated": True,
            "username": user.get_username(),
            "isStaff": user.is_staff,
        }
    )


@csrf_protect
@require_POST
def logout_view(request: HttpRequest) -> JsonResponse:
    logout(request)
    return JsonResponse({"isAuthenticated": False})
