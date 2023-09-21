from django import forms
from django.core.validators import FileExtensionValidator


class FbLibCsvForm(forms.Form):
    CSV_FILES_TYPES = (
        ('fb_ads_lib', 'FaceBook Ads Library'),
        ('hz', 'Другой'),
    )
    csv_file_type = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-select"},
        ),
        choices=CSV_FILES_TYPES,
    )
    csv_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['csv']),],
        widget=forms.FileInput(
            attrs={'class': "form-control"})
    )