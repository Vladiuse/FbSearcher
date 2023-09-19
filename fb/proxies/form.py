from .models import Proxy
from django import forms
class ProxyForm(forms.ModelForm):

    error_text = forms.CharField(widget=forms.Textarea(attrs={"disabled":"disabled"}))

    class Meta:
        model = Proxy
        fields =  ['id', 'data',  'status','error_text']