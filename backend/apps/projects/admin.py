from __future__ import annotations

import json
import re
from typing import Any

from django import forms
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Post, PostFile, PostType, Project, Tag


EXTRA_TEMPLATES: dict[str, dict[str, object]] = {
    PostType.POST: {
        "md": False,
    },
    PostType.ANIME: {
        "original_title": "",
        "season": "",
        "rating": None,
        "result": "",
    },
    PostType.ABANDONED: {
        "rating": None,
        "location": {
            "latitude": None,
            "longitude": None,
            "link": "",
        },
        "uniqueness": None,
        "monumentality": None,
        "atmosphere": None,
        "liveliness": None,
    },
}


class PostAdminForm(forms.ModelForm):
    extra = forms.JSONField(
        required=False,
        empty_value={},
        widget=forms.Textarea(
            attrs={
                "cols": 80,
                "rows": 12,
                "spellcheck": "false",
            }
        ),
    )

    class Meta:
        model = Post
        fields = "__all__"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        templates = {
            str(project_id): EXTRA_TEMPLATES.get(post_type, {})
            for project_id, post_type in Project.objects.values_list(
                "id",
                "post_type",
            )
        }
        self.fields["extra"].widget.attrs["data-project-extra-templates"] = (
            json.dumps(templates, ensure_ascii=False)
        )


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
        js = ("projects/admin/post_extra.js",)
