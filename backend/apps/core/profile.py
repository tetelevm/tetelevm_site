from __future__ import annotations

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import File, Profile


class ProfileView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    http_method_names = ("get", "head", "options")

    def get(self, request: Request, language: str) -> Response:
        if language not in {"ru", "en"}:
            raise Http404
        profile = get_object_or_404(Profile, language=language)
        data = dict(profile.data)
        file_ids = [
            data[key]
            for key in ("photoFile", "resumePreviewFile", "resumeFile")
            if data.get(key)
        ]
        files = {
            str(file.pk): file.link for file in File.objects.filter(pk__in=file_ids)
        }
        data["photoUrl"] = files.get(data.pop("photoFile", None))
        data["resumePreviewUrl"] = files.get(data.pop("resumePreviewFile", None))
        data["resumeUrl"] = files.get(data.pop("resumeFile", None))
        email = data["contacts"]["email"]
        if email["url"]:
            email["url"] = f"mailto:{email['url']}"
        return Response(data, headers={"Cache-Control": "no-store"})
