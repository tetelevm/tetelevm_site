from django.db.transaction import atomic
from django.db.models import F, Func, IntegerField, Value
from django.db.models.functions import Cast

from apps.core.models import File
from apps.projects.models import Post, PostFile, Project, Tag


def _order_photos(q):
    return q.annotate(
        order=Cast(
            Func(
                F("original_name"),
                Value(r"^.*_(\d+)\.[^.]+$"),
                Value(r"\1"),
                function="regexp_replace",
            ),
            IntegerField(),
        ),
    ).order_by("order")


@atomic
def import_posts(posts):
    for p in posts:
        project = Project.objects.get(link="mokhetiale")
        post = Post.objects.create(
            project=project,
            number=p["number"],
            text=p["text"],
        )
        files = File.objects.filter(original_name__in=p["photos"])
        for (n, f) in enumerate(_order_photos(files)):
            PostFile.objects.create(post=post, file=f, order=n)
        for t in p["tags"]:
            tag = Tag.objects.get(code=t)
            post.tags.add(tag)
        print(p["number"])
