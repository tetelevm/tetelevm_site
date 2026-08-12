from pathlib import Path

from django.contrib import admin

from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "uploaded_at")
    list_display = ("id", "filename", "uploaded_at")

    @admin.display(description="Filename")
    def filename(self, obj):
        return Path(obj.content.name).name
