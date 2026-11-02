from __future__ import annotations

from typing import Any

from django import forms
from django.core.validators import URLValidator
from django.urls import reverse
from django.utils.html import format_html

from .models import File, FileType

CONTACT_KEYS = (
    "telegram",
    "email",
    "linkedin",
    "github",
    "channel",
    "instagram",
    "linktree",
)
TEXT_FIELDS = ("name", "role", "about")


class ProfileContentForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=120)
    role = forms.CharField(label="Профессия", max_length=120)
    about = forms.CharField(label="Обо мне", required=False, widget=forms.Textarea)
    lookingForWork = forms.BooleanField(label="Ищу работу", required=False)
    photoFile = forms.ModelChoiceField(
        label="Фото", queryset=File.objects.none(), required=False
    )
    resumePreviewFile = forms.ModelChoiceField(
        label="Картинка превью резюме", queryset=File.objects.none(), required=False
    )
    resumeFile = forms.ModelChoiceField(
        label="PDF-резюме", queryset=File.objects.none(), required=False
    )

    for key in CONTACT_KEYS:
        locals()[f"{key}_value"] = forms.CharField(
            label=f"{key}: отображаемый адрес", required=False, max_length=255
        )
        field = forms.EmailField if key == "email" else forms.URLField
        locals()[f"{key}_url"] = field(
            label=f"{key}: адрес",
            required=False,
            **(
                {}
                if key == "email"
                else {
                    "assume_scheme": "https",
                    "validators": [URLValidator(schemes=["http", "https"])],
                }
            ),
        )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for key in ("photoFile", "resumePreviewFile", "resumeFile"):
            self.fields[key].help_text = format_html(
                '<a href="{}" target="_blank" rel="noopener">Загрузить файл в библиотеку</a>, затем обновите форму и выберите его.',
                reverse("admin:core_file_add"),
            )
        self.fields["photoFile"].queryset = File.objects.filter(
            file_type=FileType.PHOTO
        ).order_by("label")
        self.fields["resumePreviewFile"].queryset = self.fields["photoFile"].queryset
        self.fields["resumeFile"].queryset = File.objects.filter(
            content__iendswith=".pdf"
        ).order_by("label")

    def as_content(self) -> dict[str, Any]:
        data = self.cleaned_data
        return {
            **{key: data.get(key, "") for key in TEXT_FIELDS},
            "lookingForWork": data["lookingForWork"],
            "photoFile": str(data["photoFile"].pk) if data["photoFile"] else None,
            "resumeFile": str(data["resumeFile"].pk) if data["resumeFile"] else None,
            "resumePreviewFile": str(data["resumePreviewFile"].pk)
            if data["resumePreviewFile"]
            else None,
            "contacts": {
                key: {part: data[f"{key}_{part}"] for part in ("value", "url")}
                for key in CONTACT_KEYS
            },
        }


def flatten_content(data: dict[str, Any]) -> dict[str, Any]:
    flat = {
        key: data.get(key)
        for key in (
            *TEXT_FIELDS,
            "lookingForWork",
            "photoFile",
            "resumePreviewFile",
            "resumeFile",
        )
    }
    contacts = data.get("contacts", {})
    for key in CONTACT_KEYS:
        contact = contacts.get(key, {})
        for part in ("value", "url"):
            flat[f"{key}_{part}"] = contact.get(part, "")
    return flat
