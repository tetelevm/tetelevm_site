from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import File


class ContentType(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    code = models.CharField(_("Code"), max_length=64)

    class Meta:
        verbose_name = _("Content type")
        verbose_name_plural = _("Content types")

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", _("Open")
        PAUSED = "paused", _("Paused")
        CLOSED = "closed", _("Closed")

    name = models.CharField(_("Name"), max_length=255)
    link = models.CharField(_("Link"), max_length=64, unique=True)
    cover = models.ForeignKey(
        File,
        on_delete=models.PROTECT,
        verbose_name=_("Cover"),
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        verbose_name=_("Content type"),
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
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("Project"),
    )
    number = models.PositiveIntegerField(_("Number"))
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
    related_post = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="referenced_by_posts",
        verbose_name=_("Related post"),
        blank=True,
        null=True,
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
        return f"projects/{self.project.link}/{self.number}"

    def __str__(self) -> str:
        label = self.name or self.number
        return f"{self.project}: {label}"


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
