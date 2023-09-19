from django import forms
from django.core.validators import FileExtensionValidator


class FbLibCsvForm(forms.Form):
    csv_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['csv']),],
    )