from __future__ import annotations

from secrets import token_hex

from django.http import HttpRequest, HttpResponse

STATUS_CODES = {
    400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412,
    413, 414, 415, 416, 417, 418, 421, 422, 423, 424, 425, 426, 428,
    429, 431, 451,
    # Nonstandard demos; product-specific behavior is not implemented.
    419, 449, 499,
}


def make_response(code: int, request: HttpRequest) -> HttpResponse:
    content_type = "text/plain; charset=utf-8"
    match code:
        case 400:
            # Bad Request — the request cannot be processed as received.
            return HttpResponse(
                "Error 400: Congratulations, error.",
                status=400, content_type=content_type,
            )
        case 401:
            # Unauthorized — authentication credentials are required.
            return HttpResponse(
                "Error 401: You haven't introduced yourself, although this is just a demo anyway.",
                status=401, content_type=content_type,
                headers={'WWW-Authenticate': 'Basic realm="HTTP status demo"'},
            )
        case 402:
            # Payment Required — reserved for future use.
            return HttpResponse(
                "Error 402: This request costs money.",
                status=402, content_type=content_type,
            )
        case 403:
            # Forbidden — the server refuses to fulfill the request.
            return HttpResponse(
                "Error 403: You're not allowed here.",
                status=403, content_type=content_type,
            )
        case 404:
            # Not Found — no current representation was found.
            return HttpResponse(
                "Error 404: 404",
                status=404, content_type=content_type,
            )
        case 405:
            # Method Not Allowed — the method is unsupported for this resource.
            return HttpResponse(
                "Error 405: Try again, but differently.",
                status=405, content_type=content_type,
                headers={'Allow': ''},
            )
        case 406:
            # Not Acceptable — no available representation matches the preferences.
            return HttpResponse(
                "Error 406: We can't give you what you need.",
                status=406, content_type=content_type,
            )
        case 407:
            # Proxy Authentication Required — a proxy needs credentials.
            # Required hop-by-hop headers cannot be emitted by WSGI.
            return HttpResponse(
                "Error 407: On the other hand, this isn't a proxy request.",
                status=407, content_type=content_type,
            )
        case 408:
            # Request Timeout — the complete request did not arrive in time.
            return HttpResponse(
                "Error 408: Try something smaller.",
                status=408, content_type=content_type,
            )
        case 409:
            # Conflict — the request conflicts with the resource state.
            return HttpResponse(
                "Error 409: You're not the only one changing things around here.",
                status=409, content_type=content_type,
            )
        case 410:
            # Gone — the resource is no longer available, likely permanently.
            return HttpResponse(
                "Error 410: We've removed this endpoint.",
                status=410, content_type=content_type,
            )
        case 411:
            # Length Required — a defined Content-Length is required.
            if "Content-Length" in request.headers:
                return HttpResponse(
                    "All OK, thanks for the request!", status=200,
                    content_type=content_type,
                )
            return HttpResponse(
                "Error 411: Please specify Content-Length.",
                status=411, content_type=content_type,
            )
        case 412 | 428:
            # Synthetic failure: check presence, without evaluating conditions.
            if not any(
                header in request.headers
                for header in (
                    "If-Match", "If-None-Match",
                    "If-Modified-Since", "If-Unmodified-Since",
                )
            ):
                return HttpResponse(
                    "Error 428: Please provide a condition.",
                    status=428, content_type=content_type,
                )
            return HttpResponse(
                "Error 412: We can't meet your conditions.",
                status=412, content_type=content_type,
            )
        case 413:
            # Content Too Large — the request content exceeds the accepted size.
            return HttpResponse(
                "Error 413: It's So Fucking Big.",
                status=413, content_type=content_type,
            )
        case 414:
            # URI Too Long — the request target exceeds the accepted length.
            return HttpResponse(
                "Error 414: It's So Fucking Long.",
                status=414, content_type=content_type,
            )
        case 415:
            # Unsupported Media Type — the request content format is unsupported.
            return HttpResponse(
                "Error 415: We can't read this format.",
                status=415, content_type=content_type,
            )
        case 416:
            # Synthetic empty resource: a requested range is unavailable.
            if "Range" not in request.headers:
                return HttpResponse(
                    "All OK, thanks for the request!", status=200,
                    content_type=content_type,
                )
            return HttpResponse(
                "Error 416: RangeError",
                status=416, content_type=content_type,
                headers={'Content-Range': 'bytes */0'},
            )
        case 417:
            # Expectation Failed — the Expect requirement cannot be met.
            if "Expect" not in request.headers:
                return HttpResponse(
                    "All OK, thanks for the request!", status=200,
                    content_type=content_type,
                )
            return HttpResponse(
                "Error 417: We can't meet your expectations.",
                status=417, content_type=content_type,
            )
        case 418:
            # I'm a teapot — the traditional teapot demonstration.
            return HttpResponse(
                "       (\n"
                "         )\n"
                "     ___o___\n"
                "    /_______\\\n"
                "   /         \\\n"
                " /|           \\___\n"
                "( (           /__/\n"
                " \\_\\         /\n"
                "    \\_______/\n",
                status=418, content_type=content_type,
            )
        case 419:
            # Nonstandard Page Expired — commonly used for expired sessions or CSRF failures.
            return HttpResponse(
                "Error 419: Invalid CSRF token.",
                status=419, content_type=content_type,
            )
        case 421:
            # Misdirected Request — this server cannot serve the target origin.
            return HttpResponse(
                "Error 421: We can't reach the server :(",
                status=421, content_type=content_type,
            )
        case 422:
            # Unprocessable Content — valid syntax, unprocessable instructions.
            return HttpResponse(
                "Error 422: The data makes no sense.",
                status=422, content_type=content_type,
            )
        case 423:
            # Locked — the source or destination resource is locked.
            return HttpResponse(
                "Error 423: The resource is locked.",
                status=423, content_type=content_type,
            )
        case 424:
            # Failed Dependency — another required action failed.
            return HttpResponse(
                "Error 424: A dependent operation failed.",
                status=424, content_type=content_type,
            )
        case 425:
            # Too Early — the server will not risk processing a replayable request.
            return HttpResponse(
                "Error 425: Let's shake hands, then continue.",
                status=425, content_type=content_type,
            )
        case 426:
            # Upgrade Required — another protocol is required.
            # Required hop-by-hop headers cannot be emitted by WSGI.
            return HttpResponse(
                "Error 426: You must upgrade your protocol, but we won't tell you which one to use.",
                status=426, content_type=content_type,
            )
        case 429:
            # Too Many Requests — the client has exceeded a request limit.
            return HttpResponse(
                "Error 429: Don't repeat this request.",
                status=429, content_type=content_type,
                headers={'Retry-After': '60'},
            )
        case 431:
            # Request Header Fields Too Large — request headers exceed accepted limits.
            return HttpResponse(
                "Error 431: Read your headers yourself.",
                status=431, content_type=content_type,
            )
        case 449:
            # Nonstandard Retry With — a Microsoft extension requesting a revised request.
            if "Ms-Echo-Reply" in request.headers:
                return HttpResponse(
                    "Error 400: Bad request.",
                    status=400, content_type=content_type,
                )
            return HttpResponse(
                "Error 449: Here's your header, you forgot it!",
                status=449, content_type=content_type,
                headers={"Ms-Echo-Request": token_hex(16)},
            )
        case 451:
            # Unavailable For Legal Reasons — access is denied due to a legal demand.
            return HttpResponse(
                "The government banned the letter A\n"
                "The government bnned the letter B\n"
                "The government nned the letter D\n"
                "The government nne the letter E\n"
                "Th govrnmnt nn th lttr G\n"
                "Th ovrnmnt nn th lttr H\n"
                "T ovrnmnt nn t lttr L\n"
                "T ovrnmnt nn t ttr M\n"
                "T ovrnnt nn t ttr N\n"
                "T ovrt t ttr O\n"
                "T vrt t ttr R\n"
                "T vt t tt T\n"
                "v V\n",
                status=451, content_type=content_type,
            )
        case 499:
            # Nonstandard Client Closed Request — normally an nginx log status.
            return HttpResponse(
                "Error 499: You shouldn't see this.",
                status=499, content_type=content_type,
            )
        case _:
            return HttpResponse(status=404)
