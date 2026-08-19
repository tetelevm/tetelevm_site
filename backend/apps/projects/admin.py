from __future__ import annotations

import json
import re
from copy import deepcopy
from typing import Any

from django import forms
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Post, PostFile, PostType, Project, Tag


POST_TYPE_EXTRA_FIELDS: dict[str, tuple[str, ...]] = {
    PostType.POST: ("extra_md",),
    PostType.ANIME: (
        "extra_original_title",
        "extra_season",
        "extra_anime_rating",
        "extra_result",
    ),
    PostType.ABANDONED: (
        "extra_abandoned_rating",
        "extra_location_latitude",
        "extra_location_longitude",
        "extra_location_link",
        "extra_uniqueness",
        "extra_monumentality",
        "extra_atmosphere",
        "extra_liveliness",
    ),
}

REQUIRED_EXTRA_FIELDS: frozenset[str] = frozenset(
    {
        "extra_original_title",
        "extra_anime_rating",
        "extra_result",
        "extra_abandoned_rating",
        "extra_location_latitude",
        "extra_location_longitude",
        "extra_location_link",
        "extra_uniqueness",
        "extra_monumentality",
        "extra_atmosphere",
        "extra_liveliness",
    }
)

MANAGED_EXTRA_KEYS: frozenset[str] = frozenset(
    {
        "md",
        "original_title",
        "season",
        "rating",
        "result",
        "uniqueness",
        "monumentality",
        "atmosphere",
        "liveliness",
    }
)
MANAGED_LOCATION_KEYS: frozenset[str] = frozenset(
    {"latitude", "longitude", "link"}
)


class PostAdminForm(forms.ModelForm):
    extra_md = forms.BooleanField(
        label=_("Markdown"),
        required=False,
    )
    extra_original_title = forms.CharField(
        label=_("Оригинальное название"),
        required=False,
    )
    extra_season = forms.CharField(
        label=_("Сезон"),
        required=False,
    )
    extra_anime_rating = forms.IntegerField(
        label=_("Оценка"),
        min_value=1,
        max_value=10,
        required=False,
    )
    extra_result = forms.CharField(
        label=_("Стоит смотреть"),
        required=False,
    )
    extra_abandoned_rating = forms.FloatField(
        label=_("Оценка"),
        min_value=1,
        max_value=5,
        required=False,
    )
    extra_location_latitude = forms.FloatField(
        label=_("Широта"),
        required=False,
    )
    extra_location_longitude = forms.FloatField(
        label=_("Долгота"),
        required=False,
    )
    extra_location_link = forms.CharField(
        label=_("Ссылка на расположение"),
        required=False,
    )
    extra_uniqueness = forms.IntegerField(
        label=_("Уникальность"),
        min_value=1,
        max_value=5,
        required=False,
    )
    extra_monumentality = forms.IntegerField(
        label=_("Монументальность"),
        min_value=1,
        max_value=5,
        required=False,
    )
    extra_atmosphere = forms.IntegerField(
        label=_("Атмосфера"),
        min_value=1,
        max_value=5,
        required=False,
    )
    extra_liveliness = forms.IntegerField(
        label=_("Жизненность"),
        min_value=1,
        max_value=5,
        required=False,
    )

    class Meta:
        model = Post
        exclude = ("extra",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        post_types_by_project = {
            str(project_id): post_type
            for project_id, post_type in Project.objects.values_list(
                "id",
                "post_type",
            )
        }
        project_post_types_json = json.dumps(post_types_by_project)
        project_widget = self.fields["project"].widget
        project_widget.attrs["data-project-post-types"] = (
            project_post_types_json
        )
        wrapped_project_widget = getattr(project_widget, "widget", None)
        if wrapped_project_widget is not None:
            wrapped_project_widget.attrs["data-project-post-types"] = (
                project_post_types_json
            )

        field_post_types = {
            field_name: post_type
            for post_type, field_names in POST_TYPE_EXTRA_FIELDS.items()
            for field_name in field_names
        }
        selected_post_type = post_types_by_project.get(
            self._selected_project_id()
        )
        for field_name, post_type in field_post_types.items():
            field = self.fields[field_name]
            is_active = post_type == selected_post_type
            field.required = is_active and field_name in REQUIRED_EXTRA_FIELDS
            field.disabled = not is_active
            field.widget.attrs["data-post-extra-type"] = post_type
            field.widget.attrs["data-post-extra-required"] = (
                "true" if field_name in REQUIRED_EXTRA_FIELDS else "false"
            )

        self._set_extra_initial_values(post_types_by_project)

    def _selected_project_id(self) -> str:
        if self.is_bound:
            return str(self.data.get(self.add_prefix("project"), ""))

        project = self.initial.get("project")
        project_id = getattr(project, "pk", project)
        return str(project_id or "")

    def _set_extra_initial_values(
        self,
        post_types_by_project: dict[str, str],
    ) -> None:
        if not self.instance.pk or not isinstance(self.instance.extra, dict):
            return

        post_type = post_types_by_project.get(str(self.instance.project_id))
        extra = self.instance.extra
        if post_type == PostType.POST:
            self.initial["extra_md"] = extra.get("md", False)
            return

        if post_type == PostType.ANIME:
            self.initial.update(
                {
                    "extra_original_title": extra.get("original_title", ""),
                    "extra_season": extra.get("season", ""),
                    "extra_anime_rating": extra.get("rating"),
                    "extra_result": extra.get("result", ""),
                }
            )
            return

        if post_type != PostType.ABANDONED:
            return

        location = extra.get("location")
        if not isinstance(location, dict):
            location = {}
        self.initial.update(
            {
                "extra_abandoned_rating": extra.get("rating"),
                "extra_location_latitude": location.get("latitude"),
                "extra_location_longitude": location.get("longitude"),
                "extra_location_link": location.get("link", ""),
                "extra_uniqueness": extra.get("uniqueness"),
                "extra_monumentality": extra.get("monumentality"),
                "extra_atmosphere": extra.get("atmosphere"),
                "extra_liveliness": extra.get("liveliness"),
            }
        )

    def _extra_without_managed_values(self) -> dict[str, Any]:
        current_extra = self.instance.extra
        extra = (
            deepcopy(current_extra) if isinstance(current_extra, dict) else {}
        )
        for key in MANAGED_EXTRA_KEYS:
            extra.pop(key, None)

        location = extra.get("location")
        if not isinstance(location, dict):
            extra.pop("location", None)
            return extra

        for key in MANAGED_LOCATION_KEYS:
            location.pop(key, None)
        if not location:
            extra.pop("location")
        return extra

    def _serialized_extra(self) -> dict[str, Any]:
        extra = self._extra_without_managed_values()
        post_type = self.cleaned_data["project"].post_type
        if post_type == PostType.POST:
            extra["md"] = self.cleaned_data["extra_md"]
        elif post_type == PostType.ANIME:
            extra.update(
                {
                    "original_title": self.cleaned_data[
                        "extra_original_title"
                    ],
                    "rating": self.cleaned_data["extra_anime_rating"],
                    "result": self.cleaned_data["extra_result"],
                }
            )
            season = self.cleaned_data["extra_season"]
            if season:
                extra["season"] = season
        elif post_type == PostType.ABANDONED:
            location = extra.get("location", {})
            location.update(
                {
                    "latitude": self.cleaned_data[
                        "extra_location_latitude"
                    ],
                    "longitude": self.cleaned_data[
                        "extra_location_longitude"
                    ],
                    "link": self.cleaned_data["extra_location_link"],
                }
            )
            extra.update(
                {
                    "rating": self.cleaned_data[
                        "extra_abandoned_rating"
                    ],
                    "location": location,
                    "uniqueness": self.cleaned_data["extra_uniqueness"],
                    "monumentality": self.cleaned_data[
                        "extra_monumentality"
                    ],
                    "atmosphere": self.cleaned_data["extra_atmosphere"],
                    "liveliness": self.cleaned_data["extra_liveliness"],
                }
            )
        return extra

    def save(self, commit: bool = True) -> Post:
        self.instance.extra = self._serialized_extra()
        return super().save(commit=commit)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "link",
        "post_type",
        "post_list_type",
        "status",
        "is_public",
        "order",
    )
    list_editable = ("status", "is_public", "order")
    list_filter = ("status", "is_public", "post_type", "post_list_type")
    search_fields = ("name", "link")
    autocomplete_fields = ("cover",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 0
    fields = ("file_thumbnail", "file", "order")
    readonly_fields = ("file_thumbnail",)
    ordering = ("order",)
    autocomplete_fields = ("file",)

    @admin.display(description=_("Thumbnail"), empty_value="—")
    def file_thumbnail(self, obj: PostFile) -> str | None:
        if not obj.file_id or not obj.file.thumbnail:
            return None
        return format_html(
            '<img src="{}" alt="" width="64" height="64" loading="lazy" '
            'style="display:block;object-fit:cover;border-radius:4px">',
            obj.file.thumbnail.url,
        )

    def get_queryset(self, request: HttpRequest) -> QuerySet[PostFile]:
        return super().get_queryset(request).select_related("file")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("project", "number"),
                    "name",
                    "date",
                    "main_file",
                    "text",
                ),
                "classes": ("fieldset-custom",),
            },
        ),
        (
            None,
            {
                "fields": (
                    "extra_md",
                    "extra_original_title",
                    "extra_season",
                    "extra_anime_rating",
                    "extra_result",
                    "extra_abandoned_rating",
                    "extra_location_link",
                    "extra_location_latitude",
                    "extra_location_longitude",
                    "extra_uniqueness",
                    "extra_monumentality",
                    "extra_atmosphere",
                    "extra_liveliness",
                ),
                "classes": ("fieldset-custom", "fieldset-extra",),
            },
        ),
        (
            None,
            {
                "fields": (
                    "related_posts",
                    "tags",
                ),
                "classes": ("fieldset-custom",),
            },
        ),
    )
    list_display = ("number", "display_label", "project")
    list_filter = ("project",)
    search_fields = ("name", "text", "project__name", "number")
    ordering = ("-id",)
    autocomplete_fields = ("main_file", "related_posts", "tags")
    inlines = (PostFileInline,)

    @admin.display(description=_("Name"), ordering="name")
    def display_label(self, obj: Post) -> str:
        return obj.display_label

    def get_queryset(self, request: HttpRequest) -> QuerySet[Post]:
        return (
            super()
            .get_queryset(request)
            .select_related("project", "main_file")
            .with_display_file_counts()
        )

    def get_search_results(
        self,
        request: HttpRequest,
        queryset: QuerySet[Post],
        search_term: str,
    ) -> tuple[QuerySet[Post], bool]:
        normalized_search_term = re.sub(
            r"(?<!\w)#(?=\d+\b)",
            "",
            search_term,
        )
        return super().get_search_results(
            request,
            queryset,
            normalized_search_term,
        )

    class Media:
        css = {"all": ("projects/admin/post_form.css",)}
        js = ("projects/admin/post_extra.js",)
