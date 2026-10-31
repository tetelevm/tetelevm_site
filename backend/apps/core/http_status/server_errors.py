from __future__ import annotations

from django.http import HttpResponse

STATUS_CODES = {
    500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511,
    # Nonstandard Cloudflare demos; upstream failures are not simulated.
    520, 521, 522, 523, 524, 525, 526,
}


def make_response(code: int) -> HttpResponse:
    content_type = "text/plain; charset=utf-8"
    match code:
        case 500:
            # Internal Server Error — an unexpected server-side failure.
            return HttpResponse(
                "Error 500: Something went wrong, the server is as surprised as you are.",
                status=500, content_type=content_type,
            )
        case 501:
            # Not Implemented — the server does not support this functionality.
            return HttpResponse(
                "Error 501: Great idea, but we haven't implemented it yet.",
                status=501, content_type=content_type,
            )
        case 502:
            # Bad Gateway — an upstream server returned an invalid response.
            return HttpResponse(
                "Error 502: We asked the upstream server, and its answer made no sense.",
                status=502, content_type=content_type,
            )
        case 503:
            # Service Unavailable — temporarily unable to handle the request.
            return HttpResponse(
                "Error 503: The server is taking a little break.",
                status=503, content_type=content_type,
                headers={"Retry-After": "60"},
            )
        case 504:
            # Gateway Timeout — an upstream server did not answer in time.
            return HttpResponse(
                "Error 504: We're still waiting for the upstream server.",
                status=504, content_type=content_type,
            )
        case 505:
            # HTTP Version Not Supported — the HTTP version is unsupported.
            return HttpResponse(
                "Error 505: We speak HTTP, but apparently not your dialect. "
                "For this request, we don't understand any standard.",
                status=505, content_type=content_type,
            )
        case 506:
            # Variant Also Negotiates — a variant is itself a negotiating resource.
            return HttpResponse(
                "Error 506: We chose a variant, but uhh... Have a RecursionError.",
                status=506, content_type=content_type,
            )
        case 507:
            # Insufficient Storage — unable to store the required representation.
            return HttpResponse(
                "Error 507: Hey, you've got some free space, right? "
                "Could you spare some for me?\n🧔\n"
                "That would really help me send a response.",
                status=507, content_type=content_type,
            )
        case 508:
            # Loop Detected — a WebDAV operation encountered an infinite loop.
            return HttpResponse(
                "Error 508: We "
                + ", then ".join("processed the request" for _ in range(100))
                + ", then... Error",
                status=508, content_type=content_type,
            )
        case 509:
            # Nonstandard Bandwidth Limit Exceeded — not an assigned HTTP status.
            return HttpResponse(
                "Error 509: No bytes left for a response.",
                status=509, content_type=content_type,
            )
        case 510:
            # Not Extended — obsolete HTTP extension requirements were not met.
            return HttpResponse(
                "Error 510: We're not extended enough. But that can't be fixed.",
                status=510, content_type=content_type,
            )
        case 511:
            # Network Authentication Required — a captive portal requires login.
            return HttpResponse(
                "Error 511: You need to log in first.",
                status=511, content_type=content_type,
            )
        case 520 | 521 | 522 | 523 | 524 | 525 | 526:
            return HttpResponse(
                f"Error {code}: Although we're not Cloudflare.",
                status=code, content_type=content_type,
            )
        case _:
            return HttpResponse(status=404)
