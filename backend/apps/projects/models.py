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
    order = models.PositiveIntegerField(_("Order"), default=0)

    class Meta:
        ordering = ("order", "id")
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self) -> str:
        return self.name
