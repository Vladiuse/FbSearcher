from django.forms import ModelForm
from .models import CountryLanguage


class CountryLanguageForm(ModelForm):

    class Meta:
        fields = ['keys_deep', 'weight']
