from __future__ import annotations

from gzip import compress
from hashlib import sha256
from random import randint
from re import fullmatch

from django.http import HttpRequest, HttpResponse
from django.utils.cache import get_conditional_response
from django.utils.http import parse_etags, parse_header_parameters

STATUS_CODES = {200, 201, 202, 203, 204, 205, 206, 207, 208, 226}

FRIDGE_VERSIONS = {
    "1": (
        b"How do you put an elephant in a refrigerator?\n"
        b"1. Open the refrigerator.\n"
        b"2. Put the elephant inside.\n"
        b"3. Close the refrigerator.\n"
    ),
    "2": (
        b"How do you put a giraffe in a refrigerator?\n"
        b"1. Open the refrigerator.\n"
        b"2. Take the elephant out.\n"
        b"3. Put the giraffe inside.\n"
        b"4. Close the refrigerator.\n"
    ),
}
FRIDGE_ETAGS = {
    version: f'"{sha256(content).hexdigest()}"'
    for version, content in FRIDGE_VERSIONS.items()
}
# Fixed diff -e output: no external executable is needed by the server.
FRIDGE_DELTAS = {
    ("1", "2"): (
        b"3,4c\n2. Take the elephant out.\n3. Put the giraffe inside.\n"
        b"4. Close the refrigerator.\n.\n"
        b"1c\nHow do you put a giraffe in a refrigerator?\n.\n"
    ),
    ("2", "1"): (
        b"3,5c\n2. Put the elephant inside.\n3. Close the refrigerator.\n.\n"
        b"1c\nHow do you put an elephant in a refrigerator?\n.\n"
    ),
}


def _accepted_manipulations(value: str) -> dict[str, float]:
    accepted = {"identity": 1.0, "gzip": 0.0, "diffe": 0.0}
    seen: set[str] = set()
    for item in value.split(","):
        name, parameters = parse_header_parameters(item.strip())
        if name not in accepted or parameters.keys() - {"q"}:
            continue
        quality = parameters.get("q", "1")
        if not fullmatch(r"(?:0(?:\.[0-9]{0,3})?|1(?:\.0{0,3})?)", quality):
            continue
        # Treat a repeated refusal conservatively rather than bypassing q=0.
        accepted[name] = (
            min(accepted[name], float(quality)) if name in seen else float(quality)
        )
        seen.add(name)
    return accepted


def make_response(code: int, request: HttpRequest) -> HttpResponse:
    content_type = "text/plain; charset=utf-8"
    match code:
        case 200:
            # OK — successful response.
            return HttpResponse(
                "All OK, thanks for the request!", status=200,
                content_type=content_type,
            )
        case 201:
            # Created — a new resource has been created.
            return HttpResponse(
                "All OK, we've added you to our special little book.", status=201,
                headers={"Location": "/r/200/"}, content_type=content_type,
            )
        case 202:
            # Accepted — processing has been accepted but is not complete.
            return HttpResponse(
                f"Processing, {randint(0, 100)}% complete.", status=202,
                content_type=content_type,
            )
        case 203:
            # Non-Authoritative Information — a proxy has transformed the content.
            return HttpResponse(
                "All OK, the proxy delivered this content [DELETED]correctly.",
                status=203,
                content_type=content_type,
            )
        case 204:
            # No Content — successful response without a body.
            return HttpResponse(status=204)
        case 205:
            # Reset Content — the client should reset its input view.
            return HttpResponse(status=205)
        case 206:
            # Partial Content — the response stops in the middle of a word.
            full_content = b"Request successfully processed."
            partial_content = b"Request successfully proces"
            return HttpResponse(
                partial_content, status=206, content_type=content_type,
                headers={
                    "Content-Range": (
                        f"bytes 0-{len(partial_content) - 1}/{len(full_content)}"
                    ),
                },
            )
        case 207:
            # Multi-Status — results for multiple WebDAV operations.
            return HttpResponse(
                '<?xml version="1.0" encoding="utf-8"?>\n'
                '<multistatus xmlns="DAV:">\n'
                '  <response>\n'
                '    <href>/r/207/</href>\n'
                '    <status>HTTP/1.1 200 OK</status>\n'
                '    <responsedescription>This response.</responsedescription>\n'
                '  </response>\n'
                '</multistatus>\n',
                status=207, content_type="application/xml; charset=utf-8",
            )
        case 208:
            # Already Reported — a WebDAV binding was reported earlier.
            # Both URLs resolve to this handler; their resource IDs are identical.
            # The 208 belongs inside propstat, while the HTTP status remains 207.
            responses = "".join(
                '  <response>\n'
                f'    <href>{href}</href>\n'
                '    <propstat>\n'
                '      <prop>\n'
                '        <displayname>This response.</displayname>\n'
                '        <resourcetype><collection/></resourcetype>\n'
                '        <resource-id>\n'
                '          <href>urn:uuid:53180008-1337-1488-acab-67cofffeee69</href>\n'
                '        </resource-id>\n'
                '      </prop>\n'
                f'      <status>HTTP/1.1 {status}</status>\n'
                '    </propstat>\n'
                '  </response>\n'
                for href, status in (
                    ("/r/208/", "200 OK"),
                    ("/r/0208/", "208 Already Reported"),
                )
            )
            return HttpResponse(
                '<?xml version="1.0" encoding="utf-8"?>\n'
                '<multistatus xmlns="DAV:">\n'
                + responses
                + '</multistatus>\n',
                status=207, content_type="application/xml; charset=utf-8",
            )
        case 226:
            # IM Used — instance manipulations were applied to the representation.
            vary = "A-IM, X-Fridge-Version"
            version = request.headers.get("X-Fridge-Version", "2")
            if version not in FRIDGE_VERSIONS:
                return HttpResponse(
                    "Unknown fridge version. Choose 1 or 2.", status=400,
                    content_type=content_type, headers={"Vary": vary},
                )

            accepted = _accepted_manipulations(request.headers.get("A-IM", ""))
            base_etags = parse_etags(request.headers.get("If-None-Match", ""))
            base_version = next(
                (
                    candidate for candidate, etag in FRIDGE_ETAGS.items()
                    if candidate != version and etag in base_etags
                ),
                None,
            )
            # A delta requires a known base; gzip and identity need no history.
            available = {"identity": accepted["identity"], "gzip": accepted["gzip"]}
            if base_version is not None:
                available["diffe"] = accepted["diffe"]
            if max(available.values()) == 0:
                return HttpResponse(
                    "You must send a headers.", status=406,
                    content_type=content_type, headers={"Vary": vary},
                )

            content = FRIDGE_VERSIONS[version]
            etag = FRIDGE_ETAGS[version]
            response = HttpResponse(
                content, content_type=content_type,
                headers={"ETag": etag, "Vary": vary},
            )
            response = get_conditional_response(
                request, etag=etag, response=response,
            )
            if response.status_code == 200:
                quality = max(available.values())
                if base_version is not None and available["diffe"] == quality:
                    response.content = FRIDGE_DELTAS[base_version, version]
                    response.status_code = 226
                    response["IM"] = "diffe"
                    response["Delta-Base"] = FRIDGE_ETAGS[base_version]
                elif available["gzip"] == quality:
                    response.content = compress(content, mtime=0)
                    response.status_code = 226
                    response["IM"] = "gzip"
            return response
        case _:
            return HttpResponse(status=404)
