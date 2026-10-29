from __future__ import annotations

from django.db import transaction
from django.db.models import F

from apps.projects.models import Post, Project

BATCH_SIZE = 500


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


@transaction.atomic
def renumber_published_posts_by_date(project_code: str) -> int:
    project = Project.objects.get(link=project_code)
    posts = list(
        project.posts.published().order_by(
            F("date").asc(nulls_last=True), "number", "id"
        )
    )
    changed = sum(
        post.number != expected
        for expected, post in enumerate(posts, start=1)
    )
    if not changed:
        print("Нумерация уже соответствует датам")
        return 0

    temporary_start = max(post.number for post in posts) + len(posts) + 1
    for index, post in enumerate(posts):
        post.number = temporary_start + index
    Post.objects.bulk_update(posts, ("number",), batch_size=BATCH_SIZE)

    for number, post in enumerate(posts, start=1):
        post.number = number
    Post.objects.bulk_update(posts, ("number",), batch_size=BATCH_SIZE)

    print(f"Перенумеровано постов по дате: {changed}")
    return changed
