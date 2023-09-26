from django import forms
from .models import FbAccount
from proxies.models import Proxy
from django.db.models import Q

class FbAccountForm(forms.ModelForm):

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proxy'].queryset = self.fields['proxy'].queryset.filter(
            Q(fbaccount__isnull=True)| Q(fbaccount=kwargs['instance'])
        )

    class Meta:
        model = FbAccount
        fields = '__all__'
