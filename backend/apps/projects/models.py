from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import File, FileType


class PostType(models.TextChoices):
    POST = "post", _("Post")
    PHOTO = "photo", _("Photo")
    TRAVEL = "travel", _("Travel")
    TEXT = "text", _("Text")
    TEXT_MD = "text_md", _("Markdown text")
    DOOR = "door", _("Door")
    ANIME = "anime", _("Anime")
    PLASTICINE = "plasticine", _("Plasticine")
    ABANDONED = "abandoned", _("Abandoned")


class PostListType(models.TextChoices):
    POST = "post", _("Post")
    PHOTO = "photo", _("Photo")
    TRAVEL = "travel", _("Travel")
    TEXT = "text", _("Text")
    TEXT_MD = "text_md", _("Markdown text")
    DOOR = "door", _("Door")
    ANIME = "anime", _("Anime")
    PLASTICINE = "plasticine", _("Plasticine")
    ABANDONED = "abandoned", _("Abandoned")


DISPLAY_FILE_TYPES: tuple[tuple[str, str, str], ...] = (
    (FileType.PHOTO, "📷", "display_photo_count"),
    (FileType.VIDEO, "🎬", "display_video_count"),
    (FileType.AUDIO, "🎵", "display_audio_count"),
    (FileType.OTHER, "📎", "display_other_count"),
)


def display_file_count(file_type: str) -> models.Expression:
    additional_files = models.Q(post_files__file__file_type=file_type) & (
        models.Q(main_file_id__isnull=True)
        | ~models.Q(post_files__file_id=models.F("main_file_id"))
    )
    return models.Count(
        "post_files__file_id",
        filter=additional_files,
        distinct=True,
    ) + models.Case(
        models.When(main_file__file_type=file_type, then=models.Value(1)),
        default=models.Value(0),
        output_field=models.IntegerField(),
    )


class PostQuerySet(models.QuerySet["Post"]):
    def with_display_file_counts(self) -> PostQuerySet:
        return self.annotate(
            **{
                attribute: display_file_count(file_type)
                for file_type, _emoji, attribute in DISPLAY_FILE_TYPES
            }
        )

    def with_adjacent_post_ids(self) -> PostQuerySet:
        previous_posts = self.model.objects.filter(
            project_id=models.OuterRef("project_id"),
            number__lt=models.OuterRef("number"),
        ).order_by("-number", "-id")
        next_posts = self.model.objects.filter(
            project_id=models.OuterRef("project_id"),
            number__gt=models.OuterRef("number"),
        ).order_by("number", "id")
        return self.annotate(
            previous_post_id=models.Subquery(
                previous_posts.values("id")[:1]
            ),
            next_post_id=models.Subquery(next_posts.values("id")[:1]),
        )


class Project(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", _("Open")
        PAUSED = "paused", _("Paused")
        CLOSED = "closed", _("Closed")

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    link = models.CharField(_("Link"), max_length=64, unique=True)
    cover = models.ForeignKey(
        File,
        on_delete=models.PROTECT,
        verbose_name=_("Cover"),
    )
    post_type = models.CharField(
        _("Post type"),
        max_length=16,
        choices=PostType.choices,
        default=PostType.POST,
    )
    post_list_type = models.CharField(
        _("Post list type"),
        max_length=16,
        choices=PostListType.choices,
        default=PostListType.POST,
    )
    is_public = models.BooleanField(_("Public"), default=True)
    status = models.CharField(
        _("Status"),
        max_length=16,
        choices=Status.choices,
        default=Status.OPEN,
    )
    order = models.PositiveIntegerField(_("Order"), default=0)

    class Meta:
        ordering = ("order", "id")
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    code = models.CharField(_("Code"), max_length=64, unique=True)
    name = models.CharField(_("Name"), max_length=64)

    class Meta:
        ordering = ("name", "id")
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    objects = PostQuerySet.as_manager()

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("Project"),
    )
    number = models.PositiveIntegerField(_("Number"))
    date = models.DateField(_("Date"), blank=True, null=True)
    name = models.CharField(_("Name"), max_length=255, blank=True)
    text = models.TextField(_("Text"), blank=True)
    main_file = models.ForeignKey(
        File,
        on_delete=models.SET_NULL,
        related_name="main_for_posts",
        verbose_name=_("Main file"),
        blank=True,
        null=True,
    )
    extra = models.JSONField(_("Extra"), default=dict, blank=True)
    related_posts = models.ManyToManyField(
        "self",
        symmetrical=True,
        verbose_name=_("Related posts"),
        blank=True,
    )
    files = models.ManyToManyField(
        File,
        through="PostFile",
        related_name="posts",
        verbose_name=_("Files"),
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="posts",
        verbose_name=_("Tags"),
        blank=True,
    )

    class Meta:
        ordering = ("number", "id")
        constraints = [
            models.UniqueConstraint(
                fields=("project", "number"),
                name="unique_post_number_per_project",
            ),
        ]
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    @property
    def link(self) -> str:
        return f"/projects/{self.project.link}/{self.number}/"

    @property
    def display_label(self) -> str:
        name = self.name.strip()
        if name:
            return name

        excerpt = " ".join(self.text.split())
        if excerpt:
            return (
                excerpt
                if len(excerpt) <= 90
                else f"{excerpt[:87].rstrip()}..."
            )

        counts = self._display_file_counts()
        parts = [
            f"{emoji} {counts[file_type]}"
            for file_type, emoji, _attribute in DISPLAY_FILE_TYPES
            if counts[file_type]
        ]
        return " · ".join(parts) or "🌀"

    def _display_file_counts(self) -> dict[str, int]:
        attributes = [attribute for _type, _emoji, attribute in DISPLAY_FILE_TYPES]
        if not all(hasattr(self, attribute) for attribute in attributes):
            if self.pk is None:
                return {
                    file_type: 0
                    for file_type, _emoji, _attribute in DISPLAY_FILE_TYPES
                }

            annotated_counts = (
                type(self).objects.with_display_file_counts()
                .values(*attributes)
                .get(pk=self.pk)
            )
            for attribute, value in annotated_counts.items():
                setattr(self, attribute, value)

        return {
            file_type: int(getattr(self, attribute))
            for file_type, _emoji, attribute in DISPLAY_FILE_TYPES
        }

    def __str__(self) -> str:
        return f"{self.project}: #{self.number} — {self.display_label}"


class PostFile(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="post_files",
        verbose_name=_("Post"),
    )
    file = models.ForeignKey(
        File,
        on_delete=models.PROTECT,
        related_name="post_files",
        verbose_name=_("File"),
    )
    order = models.PositiveIntegerField(_("Order"), default=0)

    class Meta:
        ordering = ("order", "id")
        constraints = [
            models.UniqueConstraint(
                fields=("post", "file"),
                name="unique_file_per_post",
            ),
            models.UniqueConstraint(
                fields=("post", "order"),
                name="unique_file_order_per_post",
            ),
        ]
        verbose_name = _("Post file")
        verbose_name_plural = _("Post files")

    def __str__(self) -> str:
        return f"{self.post}: {self.file}"
