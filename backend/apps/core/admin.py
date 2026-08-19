from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    readonly_fields = (
        "image_preview",
        "id",
        "original_name",
        "file_type",
        "preview",
        "thumbnail",
        "uploaded_at",
    )
    list_display = (
        "thumbnail_preview",
        "id",
        "original_name",
        "file_type",
        "uploaded_at",
    )
    list_filter = ("file_type",)
    search_fields = ("original_name",)
    ordering = ("-uploaded_at",)

    @admin.display(description=_("Thumbnail"), empty_value="—")
    def thumbnail_preview(self, obj: File) -> str | None:
        if not obj.thumbnail:
            return None
        return format_html(
            '<img src="{}" alt="" width="64" height="64" loading="lazy" '
            'style="display:block;object-fit:cover;border-radius:4px">',
            obj.thumbnail.url,
        )

    @admin.display(description=_("Preview"), empty_value="—")
    def image_preview(self, obj: File) -> str | None:
        if not obj.preview:
            return None
        return format_html(
            '<img src="{}" alt="" '
            'style="display:block;max-width:100%;width:auto;height:auto;'
            'max-height:600px;border-radius:4px">',
            obj.preview.url,
        )
