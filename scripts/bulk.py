from datetime import date

from django.db.transaction import atomic
from django.db.models import F, Func, IntegerField, Value
from django.db.models.functions import Cast

from apps.core.models import File
from apps.projects.models import Post, PostFile, Project, Tag


def _order_photos(q):
    return q.annotate(
        order=Cast(
            Func(
                F("label"),
                Value(r"^.*_(\d+)\.[^.]+$"),
                Value(r"\1"),
                function="regexp_replace",
            ),
            IntegerField(),
        ),
    ).order_by("order")


@atomic
def import_mokhetiale(posts):
    for p in posts:
        project = Project.objects.get(link="mokhetiale")
        post = Post.objects.create(
            project=project,
            number=p["number"],
            text=p["text"],
        )
        files = File.objects.filter(label__in=p["photos"])
        for (n, f) in enumerate(_order_photos(files)):
            PostFile.objects.create(post=post, file=f, order=n)
        for t in p["tags"]:
            tag = Tag.objects.get(code=t)
            post.tags.add(tag)
        print(p["number"])


@atomic
def import_shenishvnebi(posts: list[dict[str, object]]) -> None:
    project = Project.objects.get(link="shenishvnebi")

    for data in posts:
        post = Post.objects.create(
            project=project,
            number=int(data["number"]),
            date=date.fromisoformat(str(data["date"])),
            text=str(data.get("text", "")),
        )
        files = File.objects.filter(
            label__in=data.get("photos", []),
        )
        for order, file in enumerate(_order_photos(files)):
            PostFile.objects.create(post=post, file=file, order=order)
        for code in data.get("tags", []):
            post.tags.add(Tag.objects.get(code=code))
        print(post.number)
