from __future__ import annotations

import json
from typing import Any

from django import forms
from django.contrib import admin

from .models import Post, PostFile, PostType, Project, Tag


EXTRA_TEMPLATES: dict[str, dict[str, object]] = {
    PostType.ANIME: {
        "original_title": "",
        "rating": None,
        "result": "",
    },
    PostType.ABANDONED: {
        "rating": None,
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
    ordering = ("order",)
    autocomplete_fields = ("file",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ("number", "name", "project")
    list_filter = ("project",)
    search_fields = ("name", "text")
    ordering = ("-id",)
    autocomplete_fields = ("main_file", "related_post", "tags")
    inlines = (PostFileInline,)

    class Media:
        js = ("projects/admin/post_extra.js",)
