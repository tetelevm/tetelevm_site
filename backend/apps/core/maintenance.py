from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.db.models import Exists, OuterRef, QuerySet

from .models import File


def tidy_media() -> int:
    root = Path(settings.MEDIA_ROOT)
    used = {
        name
        for row in File.objects.values_list("content", "thumbnail")
        for name in row
        if name
    }
    unused = [
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.name != ".gitkeep"
        and path.relative_to(root).as_posix() not in used
    ]
    for path in unused:
        path.unlink()
    return len(unused)


def find_orphan_files() -> QuerySet[File]:
    from apps.projects.models import Post, PostFile, Project

    return File.objects.alias(
        used_as_main=Exists(Post.objects.filter(main_file_id=OuterRef("pk"))),
        used_as_attachment=Exists(PostFile.objects.filter(file_id=OuterRef("pk"))),
        used_as_cover=Exists(Project.objects.filter(cover_id=OuterRef("pk"))),
    ).filter(used_as_main=False, used_as_attachment=False, used_as_cover=False)
