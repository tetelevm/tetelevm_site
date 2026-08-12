from pathlib import Path

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "uploaded_at")
    list_display = ("id", "filename", "uploaded_at")

    @admin.display(description=_("Filename"))
    def filename(self, obj: File) -> str:
        return Path(obj.content.name).name
