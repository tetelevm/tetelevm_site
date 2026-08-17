from django.contrib import admin

from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "original_name",
        "file_type",
        "preview",
        "thumbnail",
        "uploaded_at",
    )
    list_display = ("id", "original_name", "file_type", "uploaded_at")
    list_filter = ("file_type",)
    search_fields = ("original_name",)
    ordering = ("-uploaded_at",)
