import re
from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from countries.models import Country


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
        (FB_7_DAYS_TYPE, 'Country stat'),
        (FB_ADS_LIB_TYPE, 'FaceBook Ads Library keys'),
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
    add_low_spend = forms.BooleanField(required=False,)


class TxtFileForm(forms.Form):
    """
    Загруска групп из txt файла
    """
    txt_files = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['txt']), ],
        widget=forms.FileInput(
            attrs={'class': "form-control"})
    )
    add_in_stat = forms.BooleanField(required=False)

    def clean(self):
        """При созранении` статистики должны быть указана страна в имени файла"""
        cleaned_data = super().clean()
        if cleaned_data['add_in_stat']:
            not_match_file_names = []
            loaded_countries = set()
            for file in self.files.getlist("txt_files"):
                try:
                    ds, country, other = file.name.split('_')
                    loaded_countries.add(country.lower())
                except ValueError:
                    not_match_file_names.append( file.name)
            if not_match_file_names:
                raise ValidationError(
                    [ValidationError(_(f'Incorrect file name: {file_name}'), code='error') for file_name in not_match_file_names]
                )
            countries_in_db = Country.objects.filter(pk__in=loaded_countries).values('pk')
            if len(countries_in_db) != len(loaded_countries):
                if_bd_exists_codes = set([country['pk'] for country in countries_in_db])
                incorrect_codes = loaded_countries - if_bd_exists_codes
                raise ValidationError(
                    [ValidationError(_(f'Incorrect country iso code in file name: {incorrecr}!')) for incorrecr in incorrect_codes]
                )
        return cleaned_data