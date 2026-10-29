from __future__ import annotations

from pathlib import Path

from django.db import transaction
from django.db.models import Prefetch

from apps.core.models import File

from .models import Post, PostFile

BATCH_SIZE = 500


@transaction.atomic
def relabel_project_files() -> int:
    post_files = Prefetch(
        "post_files",
        queryset=PostFile.objects.select_related("file").order_by(
            "order",
            "id",
        ),
    )
    posts = (
        Post.objects.select_related("project", "main_file")
        .prefetch_related(post_files)
        .order_by("project_id", "number", "id")
    )
    files_by_id: dict[object, File] = {}
    original_labels: dict[object, str] = {}

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
            label = f"{post.project.link}_{post_number}_{file_number}{extension}"
            original_labels.setdefault(file.pk, file.label)
            file.label = label
            files_by_id[file.pk] = file

    changed_files = [
        file
        for file_id, file in files_by_id.items()
        if file.label != original_labels[file_id]
    ]
    if changed_files:
        File.objects.bulk_update(changed_files, ("label",), batch_size=BATCH_SIZE)
    updated = len(changed_files)
    return updated
