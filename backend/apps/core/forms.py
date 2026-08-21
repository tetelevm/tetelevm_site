from __future__ import annotations

from typing import Any

from django import forms
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import gettext_lazy as _


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def clean(
        self,
        data: UploadedFile | list[UploadedFile] | None,
        initial: object = None,
    ) -> list[UploadedFile]:
        files = data if isinstance(data, (list, tuple)) else [data]
        clean_single_file = super().clean
        return [clean_single_file(file, initial) for file in files]


class BulkFileUploadForm(forms.Form):
    prefix = forms.CharField(
        label=_("Original name prefix"),
        required=False,
        max_length=255,
        help_text=_("Added before each uploaded file name."),
    )
    files = MultipleFileField(
        label=_("Files"),
        widget=MultipleFileInput(),
        help_text=_("Select all files you want to upload."),
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        prefix = cleaned_data.get("prefix", "")
        files = cleaned_data.get("files", [])
        for uploaded_file in files:
            if len(f"{prefix}{uploaded_file.name}") > 255:
                self.add_error(
                    "prefix",
                    _(
                        "Prefix and file name must contain at most 255 "
                        "characters: %(name)s"
                    )
                    % {"name": uploaded_file.name},
                )
        return cleaned_data
