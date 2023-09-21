from .models import Proxy
from django import forms
class ProxyForm(forms.ModelForm):

    error_text = forms.CharField(required=False,
                                 widget=forms.Textarea(attrs={"disabled":"disabled", }))

    class Meta:
        model = Proxy
        fields =  ['id', 'ip', 'port','protocol', 'login', 'password', 'status','error_text']