from __future__ import annotations

from django.http import HttpResponse

STATUS_CODES = {300, 301, 302, 303, 304, 305, 307, 308}


def make_response(code: int) -> HttpResponse:
    match code:
        case 300:
            # Multiple Choices — let the visitor choose a redirect example.
            choices = "".join(
                f'<li><a href="/r/{choice}/">{choice} {label}</a></li>'
                for choice, label in (
                    (301, "Moved Permanently"),
                    (302, "Found"),
                    (303, "See Other"),
                    (304, "Not Modified"),
                    (305, "Use Proxy (deprecated)"),
                    (306, "Unused (returns 404)"),
                    (307, "Temporary Redirect"),
                    (308, "Permanent Redirect"),
                )
            )
            return HttpResponse(
                '<!doctype html><html lang="en"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width, initial-scale=1">'
                '<title>300 Multiple Choices</title></head><body>'
                '<h1>300 Multiple Choices</h1><p>Choose a response:</p><ul>'
                + choices + '</ul></body></html>',
                status=300, content_type="text/html; charset=utf-8",
            )
        case 301:
            # Moved Permanently — future requests should use the new URL.
            return HttpResponse(status=301, headers={
                "Location": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            })
        case 302:
            # Found — the resource temporarily lives at another URL.
            return HttpResponse(status=302, headers={
                "Location": "https://www.youtube.com/watch?v=5qJgS1PhKW0",
            })
        case 303:
            # See Other — retrieve another resource with GET or HEAD.
            return HttpResponse(status=303, headers={
                "Location": "https://www.youtube.com/watch?v=3BFTio5296w",
            })
        case 304:
            # Not Modified — this status must not include a response body.
            return HttpResponse(status=304)
        case 305:
            # Use Proxy — deprecated; retained as a synthetic status example.
            return HttpResponse(
                "But proxies don't work here, so sorry.",
                status=305, content_type="text/plain; charset=utf-8",
            )
        case 307:
            # Temporary Redirect — follow the new URL without changing the method.
            return HttpResponse(status=307, headers={
                "Location": "https://www.youtube.com/watch?v=orbjuMHZ4k4",
            })
        case 308:
            # Permanent Redirect — preserve the method at the permanent new URL.
            return HttpResponse(status=308, headers={
                "Location": "https://www.youtube.com/watch?v=fXnxJ2bABeE",
            })
        case _:
            return HttpResponse(status=404)
