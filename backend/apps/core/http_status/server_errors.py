from __future__ import annotations

from django.http import HttpResponse

STATUS_CODES = {
    500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511,
    # Nonstandard Cloudflare placeholders; upstream failures are not simulated.
    520, 521, 522, 523, 524, 525, 526,
}


def make_response(code: int) -> HttpResponse:
    response = HttpResponse(status=code)
    if code == 503:
        response["Retry-After"] = "60"
    return response
