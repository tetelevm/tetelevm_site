from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_safe

from . import client_errors, redirects, server_errors, success


@require_safe
def status_response(request: HttpRequest, code: int) -> HttpResponse:
    for group in (success, redirects, client_errors, server_errors):
        if code in group.STATUS_CODES:
            response = (
                group.make_response(code, request)
                if group is success else group.make_response(code)
            )
            break
    else:
        response = HttpResponse(status=404)

    response["Cache-Control"] = "no-store"
    response["X-Robots-Tag"] = "noindex"
    return response
