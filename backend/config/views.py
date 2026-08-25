from __future__ import annotations

import re
from dataclasses import dataclass

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.html import escape, format_html
from django.utils.safestring import SafeString, mark_safe
from django.views.decorators.http import require_GET

from apps.core.models import FileType
from apps.projects.models import DISPLAY_FILE_TYPES, Post, Project

DESCRIPTION_LIMIT = 160
ARCHIVE_DESCRIPTION = (
    "Архив проектов tetelevm: тексты, фотографии и другие материалы."
)
PROJECT_PATH = re.compile(r"^/archive/(?P<project>[^/]+)/$")
POST_PATH = re.compile(
    r"^/archive/(?P<project>[^/]+)/(?P<number>[0-9]+)/$"
)


@dataclass(frozen=True)
class PageMetadata:
    title: str
    social_title: str
    path: str
    description: str = ""
    image: str = "/favicon.ico"
    page_type: str = "website"
    locale: str = "ru_RU"
    noindex: bool = False
    not_found: bool = False


def visible_projects(request: HttpRequest) -> QuerySet[Project]:
    projects = Project.objects.all()
    if request.user.is_authenticated:
        return projects
    return projects.filter(is_public=True)


def shortened_text(value: str, limit: int = DESCRIPTION_LIMIT) -> str:
    normalized = " ".join(value.split())
    if len(normalized) <= limit:
        return normalized
    return f"{normalized[: limit - 1].rstrip()}…"


def post_file_description(post: Post) -> str:
    counts = post._display_file_counts()
    return " · ".join(
        f"{counts[file_type]} {emoji}"
        for file_type, emoji, _attribute in DISPLAY_FILE_TYPES
        if counts[file_type]
    )


def metadata_for_path(request: HttpRequest, path: str) -> PageMetadata:
    if path == "/":
        return PageMetadata("tetelevm", "tetelevm - Main", "/")
    if path == "/archive/":
        return PageMetadata(
            "Project archive",
            "tetelevm - Archive",
            "/archive/",
            description=ARCHIVE_DESCRIPTION,
        )
    if path == "/login/":
        return PageMetadata(
            "Login",
            "tetelevm - Login",
            "/login/",
            noindex=True,
        )
    if path == "/archive/random/":
        return PageMetadata(
            "Random post",
            "tetelevm - Random post",
            "/archive/random/",
            noindex=True,
        )

    post_match = POST_PATH.fullmatch(path)
    if post_match:
        post = (
            Post.objects.with_display_file_counts()
            .select_related("project", "main_file")
            .filter(
                project__in=visible_projects(request),
                project__link=post_match["project"],
                number=int(post_match["number"]),
            )
            .first()
        )
        if post is not None:
            post_name = post.name.strip()
            short_name = post_name or f"#{post.number}"
            title = post_name or f"{post.project.name} #{post.number}"
            description = shortened_text(post.text) or post_file_description(post)
            image = "/favicon.ico"
            if (
                post.main_file is not None
                and post.main_file.file_type == FileType.PHOTO
            ):
                image = post.main_file.link
            return PageMetadata(
                title=title,
                social_title=(
                    f"tetelevm - {post.project.name} - {short_name}"
                ),
                path=post.link,
                description=description,
                image=image,
                page_type="article",
            )

    project_match = PROJECT_PATH.fullmatch(path)
    if project_match:
        project = (
            visible_projects(request)
            .select_related("cover")
            .filter(link=project_match["project"])
            .first()
        )
        if project is not None:
            return PageMetadata(
                title=project.name,
                social_title=f"tetelevm - {project.name}",
                path=f"/archive/{project.link}/",
                description=shortened_text(project.description),
                image=project.cover.link,
            )

    return PageMetadata(
        "Страница не найдена",
        "tetelevm - Страница не найдена",
        path,
        noindex=True,
        not_found=True,
    )


def caddy_template_safe(value: str) -> SafeString:
    escaped = str(escape(value))
    return mark_safe(
        escaped.replace("{", "&#123;").replace("}", "&#125;")
    )


def metadata_html(request: HttpRequest, metadata: PageMetadata) -> SafeString:
    canonical_url = request.build_absolute_uri(metadata.path)
    image_url = request.build_absolute_uri(metadata.image)
    twitter_card = (
        "summary" if metadata.image == "/favicon.ico" else "summary_large_image"
    )
    tags = [
        format_html(
            '<title data-page-meta>{}</title>',
            caddy_template_safe(metadata.title),
        ),
        format_html(
            '<link rel="canonical" href="{}" data-page-meta>',
            caddy_template_safe(canonical_url),
        ),
        format_html(
            '<meta property="og:type" content="{}" data-page-meta>',
            metadata.page_type,
        ),
        format_html(
            '<meta property="og:title" content="{}" data-page-meta>',
            caddy_template_safe(metadata.social_title),
        ),
        format_html(
            '<meta property="og:url" content="{}" data-page-meta>',
            caddy_template_safe(canonical_url),
        ),
        format_html(
            '<meta property="og:image" content="{}" data-page-meta>',
            caddy_template_safe(image_url),
        ),
        format_html(
            '<meta property="og:locale" content="{}" data-page-meta>',
            metadata.locale,
        ),
        format_html(
            '<meta name="twitter:card" content="{}" data-page-meta>',
            twitter_card,
        ),
        format_html(
            '<meta name="twitter:title" content="{}" data-page-meta>',
            caddy_template_safe(metadata.social_title),
        ),
        format_html(
            '<meta name="twitter:image" content="{}" data-page-meta>',
            caddy_template_safe(image_url),
        ),
    ]
    if metadata.noindex:
        tags.append(
            mark_safe(
                '<meta name="robots" content="noindex" data-page-meta>'
            )
        )
    if metadata.description:
        description = caddy_template_safe(metadata.description)
        tags.extend(
            (
                format_html(
                    '<meta name="description" content="{}" data-page-meta>',
                    description,
                ),
                format_html(
                    '<meta property="og:description" content="{}" '
                    "data-page-meta>",
                    description,
                ),
                format_html(
                    '<meta name="twitter:description" content="{}" '
                    "data-page-meta>",
                    description,
                ),
            )
        )
    if metadata.not_found:
        tags.append(mark_safe("{{httpError 404}}"))
    return mark_safe("\n".join(str(tag) for tag in tags))


@require_GET
def page_meta(request: HttpRequest) -> HttpResponse:
    path = request.GET.get("path", "/")
    metadata = metadata_for_path(request, path)
    return HttpResponse(metadata_html(request, metadata), content_type="text/html")


@require_GET
def robots_txt(request: HttpRequest) -> HttpResponse:
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    lines = (
        "User-agent: *",
        "Disallow: /_admin/",
        "Disallow: /_api/",
        f"Sitemap: {sitemap_url}",
    )
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")
