from .models import Proxy
from django import forms
class ProxyForm(forms.ModelForm):

    error_text_full = forms.CharField(required=False,
                                 widget=forms.Textarea(attrs={"disabled":"disabled", }))

    class Meta:
        model = Proxy
        fields = '__all__'
        # fields =  ['id', 'comment','ip', 'port','protocol', 'login', 'password', 'status','error_text']
