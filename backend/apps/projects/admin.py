from django.contrib import admin

from .models import ContentType, Project


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "link", "content_type", "is_public", "order")
    list_editable = ("is_public", "order")
    list_filter = ("is_public", "content_type")
    search_fields = ("name", "link")
