from __future__ import annotations

from django.http import HttpResponse

STATUS_CODES = {
    400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412,
    413, 414, 415, 416, 417, 418, 421, 422, 423, 424, 425, 426, 428,
    429, 431, 451,
    # Nonstandard placeholders; product-specific behavior is not implemented.
    419, 449, 499,
}


def make_response(code: int) -> HttpResponse:
    response = HttpResponse(status=code)
    if code == 401:
        response["WWW-Authenticate"] = 'Basic realm="HTTP status demo"'
    elif code == 405:
        response["Allow"] = "GET, HEAD"
    elif code == 416:
        response["Content-Range"] = "bytes */0"
    elif code == 418:
        response = HttpResponse(
            "🫖\n", status=code, content_type="text/plain; charset=utf-8",
        )
    elif code == 429:
        response["Retry-After"] = "60"
    return response
