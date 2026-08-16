from django.contrib import admin

from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "original_name",
        "preview",
        "thumbnail",
        "uploaded_at",
    )
    list_display = ("id", "original_name", "uploaded_at")
    search_fields = ("original_name",)
    ordering = ("-uploaded_at",)
