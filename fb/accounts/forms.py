from django import forms
from .models import FbAccount
from proxies.models import Proxy
from django.db.models import Q

class FbAccountForm(forms.ModelForm):

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['proxy'].queryset = self.fields['proxy'].queryset.filter(
                Q(fbaccount__isnull=True)| Q(fbaccount=kwargs['instance'])
            )
        else:
            self.fields['proxy'].queryset = self.fields['proxy'].queryset.filter(fbaccount__isnull=True)

    class Meta:
        model = FbAccount
        fields = '__all__'
