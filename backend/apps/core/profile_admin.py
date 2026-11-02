from __future__ import annotations

from typing import Any

from django import forms
from django.contrib import admin
from django.http import HttpRequest

from .models import Profile
from .profile_schema import CONTACT_KEYS, ProfileContentForm, flatten_content


class ProfileAdminForm(ProfileContentForm, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("language",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial.update(flatten_content(self.instance.data))

    def clean(self) -> dict[str, Any]:
        cleaned = super().clean()
        if not self.errors:
            self.instance.data = self.as_content()
        return cleaned


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = ("language",)

    def get_fieldsets(
        self, request: HttpRequest, obj: Profile | None = None
    ) -> tuple[Any, ...]:
        return (
            (
                None,
                {
                    "fields": (
                        "language",
                        "name",
                        "role",
                        "about",
                        "photoFile",
                        "photoPlaceholder",
                        "lookingForWork",
                        "availabilityText",
                    )
                },
            ),
            (
                "Контакты",
                {
                    "fields": (
                        "contactsTitle",
                        "contactPending",
                        *(
                            f"{key}_{part}"
                            for key in CONTACT_KEYS
                            for part in ("label", "value", "url")
                        ),
                    )
                },
            ),
            (
                "Резюме",
                {
                    "fields": (
                        "resumeFile",
                        "resumePreviewFile",
                        "resumeTitle",
                        "resumeDescription",
                        "resumePending",
                    )
                },
            ),
            ("Подвал", {"fields": ("footerCredit",)}),
        )
