from __future__ import annotations

from typing import Any

from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .forms import BulkFileUploadForm
from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    change_list_template = "admin/core/file/change_list.html"
    readonly_fields = (
        "image_preview",
        "id",
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

    def get_readonly_fields(
        self,
        request: HttpRequest,
        obj: File | None = None,
    ) -> tuple[str, ...]:
        fields = super().get_readonly_fields(request, obj)
        if obj is None:
            return (*fields, "original_name")
        return fields

    def get_urls(self) -> list[Any]:
        custom_urls = [
            path(
                "bulk-upload/",
                self.admin_site.admin_view(self.bulk_upload_view),
                name="core_file_bulk_upload",
            ),
        ]
        return custom_urls + super().get_urls()

    def bulk_upload_view(self, request: HttpRequest) -> HttpResponse:
        if not self.has_add_permission(request):
            raise PermissionDenied

        form = BulkFileUploadForm(request.POST or None, request.FILES or None)
        if request.method == "POST" and form.is_valid():
            files = form.cleaned_data["files"]
            prefix = form.cleaned_data["prefix"]
            compress_images = form.cleaned_data["compress_images"]
            for uploaded_file in files:
                file = File(content=uploaded_file)
                file.save(compress_image=compress_images)
                if prefix:
                    file.original_name = f"{prefix}{file.original_name}"
                    file.save(update_fields=("original_name",))
            self.message_user(
                request,
                _("Successfully uploaded %(count)d files.") % {"count": len(files)},
                messages.SUCCESS,
            )
            return redirect("admin:core_file_changelist")

        context = {
            **self.admin_site.each_context(request),
            "form": form,
            "opts": self.model._meta,
            "title": _("Upload multiple files"),
        }
        return TemplateResponse(
            request,
            "admin/core/file/bulk_upload.html",
            context,
        )

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
