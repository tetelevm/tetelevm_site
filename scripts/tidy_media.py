from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.db.models import Exists, OuterRef, Prefetch

from apps.core.models import File
from apps.projects.models import Post, PostFile, Project

BATCH_SIZE = 500


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
    print(f"Удалено файлов: {len(unused)}")
    return len(unused)


@transaction.atomic
def renumber_published_posts(project_code: str) -> int:
    project = Project.objects.get(link=project_code)
    posts = list(project.posts.published().order_by("number", "id"))
    changed = sum(
        post.number != expected
        for expected, post in enumerate(posts, start=1)
    )
    if not changed:
        print("Нумерация уже последовательная")
        return 0

    temporary_start = max(post.number for post in posts) + len(posts) + 1
    for index, post in enumerate(posts):
        post.number = temporary_start + index
    Post.objects.bulk_update(posts, ("number",), batch_size=BATCH_SIZE)

    for number, post in enumerate(posts, start=1):
        post.number = number
    Post.objects.bulk_update(posts, ("number",), batch_size=BATCH_SIZE)

    print(f"Перенумеровано постов: {changed}")
    return changed


def relabel_project_files(project_code: str) -> int:
    project = Project.objects.get(link=project_code)
    post_files = Prefetch(
        "post_files",
        queryset=PostFile.objects.select_related("file").order_by(
            "order",
            "id",
        ),
    )
    posts = (
        project.posts.select_related("main_file")
        .prefetch_related(post_files)
        .order_by("number", "id")
    )
    pending: dict[object, File] = {}
    updated = 0

    def flush() -> None:
        nonlocal updated
        if not pending:
            return
        files = list(pending.values())
        File.objects.bulk_update(files, ("label",), batch_size=BATCH_SIZE)
        updated += len(files)
        pending.clear()

    for post in posts.iterator(chunk_size=BATCH_SIZE):
        post_number = f"d{abs(post.number)}" if post.is_draft else str(post.number)
        files = ([post.main_file] if post.main_file else []) + [
            post_file.file for post_file in post.post_files.all()
        ]
        seen: set[object] = set()
        unique_files = []
        for file in files:
            if file.pk not in seen:
                seen.add(file.pk)
                unique_files.append(file)
        for file_number, file in enumerate(unique_files, start=1):
            extension = Path(file.content.name).suffix.lower()
            file.label = (
                f"{project_code}_{post_number}_{file_number}{extension}"
            )
            pending[file.pk] = file
            if len(pending) >= BATCH_SIZE:
                flush()

    flush()
    print(f"Обновлено меток файлов: {updated}")
    return updated


def find_orphan_files(delete: bool = False) -> int:
    orphan_files = (
        File.objects.annotate(
            used_as_main=Exists(
                Post.objects.filter(main_file_id=OuterRef("pk"))
            ),
            used_as_attachment=Exists(
                PostFile.objects.filter(file_id=OuterRef("pk"))
            ),
        )
        .filter(
            used_as_main=False,
            used_as_attachment=False,
        )
        .order_by("pk")
    )

    if not delete:
        count = 0
        for file in orphan_files.iterator(chunk_size=BATCH_SIZE):
            print(file.pk, file.label, file.content.name)
            count += 1
        print(f"Найдено непривязанных файлов: {count}")
        return count

    deleted = 0
    while True:
        batch = list(orphan_files[:BATCH_SIZE])
        if not batch:
            break
        for file in batch:
            print(file.pk, file.label, file.content.name)
        File.objects.filter(pk__in=[file.pk for file in batch]).delete()
        deleted += len(batch)

    print(f"Удалено непривязанных записей: {deleted}")
    return deleted
