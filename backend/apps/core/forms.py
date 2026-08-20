from __future__ import annotations

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
    files = MultipleFileField(
        label=_("Files"),
        widget=MultipleFileInput(),
        help_text=_("Select all files you want to upload."),
    )
