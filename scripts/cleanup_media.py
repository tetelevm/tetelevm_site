from __future__ import annotations

from pathlib import Path

from django.conf import settings

from apps.core.models import File


def cleanup_unused_media() -> int:
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
    print(f"Удалено файлов: {len(unused)}")
    return len(unused)
