from django.contrib import admin

from .models import Post, PostFile, Project, Tag


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
    list_display = ("number", "name", "project")
    list_filter = ("project",)
    search_fields = ("name", "text")
    ordering = ("-id",)
    autocomplete_fields = ("main_file", "related_post", "tags")
    inlines = (PostFileInline,)
