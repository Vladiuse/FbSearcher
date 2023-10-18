from django import forms
from django.core.validators import FileExtensionValidator


class FbLibCsvForm(forms.Form):
    csv_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['csv']),],
        widget=forms.FileInput(
            attrs={'class': "form-control"})
    )



class FbLibZipForm(forms.Form):
    FB_ADS_LIB_TYPE = 'fb_ads_lib_zip'
    FB_7_DAYS_TYPE = '7_days'
    CSV_FILES_TYPES = (
        (FB_ADS_LIB_TYPE, 'FaceBook Ads Library'),
        (FB_7_DAYS_TYPE, '7 days stat'),
    )
    zip_file_type = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': "form-select"},
        ),
        choices=CSV_FILES_TYPES,
    )
    zip_files = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['zip']),],
        widget=forms.FileInput(
            attrs={'class': "form-control"})
    )
    add_low_spend = forms.BooleanField(required=False)


class TxtFileForm(forms.Form):
    txt_files = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['txt']), ],
        widget=forms.FileInput(
            attrs={'class': "form-control"})
    )