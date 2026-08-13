from django.contrib import admin

from .models import ContentType, Post, PostFile, Project, Tag


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "link",
        "content_type",
        "status",
        "is_public",
        "order",
    )
    list_editable = ("status", "is_public", "order")
    list_filter = ("status", "is_public", "content_type")
    search_fields = ("name", "link")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 0
    ordering = ("order",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "project")
    list_filter = ("project",)
    search_fields = ("name", "text")
    ordering = ("project", "number")
    raw_id_fields = ("main_file", "related_post")
    filter_horizontal = ("tags",)
    inlines = (PostFileInline,)
