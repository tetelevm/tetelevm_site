from __future__ import annotations

from django.http import HttpResponse

STATUS_CODES = {300, 301, 302, 303, 304, 305, 307, 308}
RICKROLL_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def make_response(code: int) -> HttpResponse:
    response = HttpResponse(status=code)
    if code in {301, 302, 303, 307, 308}:
        response["Location"] = RICKROLL_URL
    return response
