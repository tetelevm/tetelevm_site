from __future__ import annotations

from django.http import FileResponse, Http404, HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_safe
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import File, Profile
from .profile_schema import CONTACT_KEYS, TEXT_FIELDS

@require_safe
def profile_resume(request: HttpRequest, language: str) -> FileResponse:
    if language not in {"ru", "en"}:
        raise Http404
    profile = get_object_or_404(Profile, language=language)
    file_id = profile.data.get("resumeFile")
    if not file_id:
        raise Http404
    file = get_object_or_404(File, pk=file_id)
    try:
        content = file.content.open("rb")
    except FileNotFoundError as exc:
        raise Http404 from exc
    return FileResponse(
        content,
        content_type="application/pdf",
        as_attachment=False,
        filename=profile.data.get("resumeFilename") or "resume.pdf",
        headers={"Cache-Control": "no-store"},
    )


class ProfileView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    http_method_names = ("get", "head", "options")

    def get(self, request: Request, language: str) -> Response:
        if language not in {"ru", "en"}:
            raise Http404
        profile = get_object_or_404(Profile, language=language)
        data = {key: profile.data.get(key, "") for key in TEXT_FIELDS}
        data["lookingForWork"] = profile.data["lookingForWork"]
        data["contacts"] = {
            key: {
                part: profile.data["contacts"].get(key, {}).get(part, "")
                for part in ("value", "url")
            }
            for key in CONTACT_KEYS
        }
        file_ids = [
            profile.data[key]
            for key in ("photoFile", "resumePreviewFile", "resumeFile")
            if profile.data.get(key)
        ]
        files = {
            str(file.pk): file.link for file in File.objects.filter(pk__in=file_ids)
        }
        data["photoUrl"] = files.get(profile.data.get("photoFile"))
        data["resumePreviewUrl"] = files.get(profile.data.get("resumePreviewFile"))
        data["resumeUrl"] = (
            reverse("profile-resume", args=[language])
            if profile.data.get("resumeFile") in files
            else None
        )
        email = data["contacts"]["email"]
        if email["url"]:
            email["url"] = f"mailto:{email['url']}"
        return Response(data, headers={"Cache-Control": "no-store"})
