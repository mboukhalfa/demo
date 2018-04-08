from django.forms import ModelForm, Textarea, Form
from oauth.models import OauthApp


class OauthAppForm(ModelForm):
    class Meta:
        model = OauthApp
        fields = ['client_id', 'client_secret', 'redirect_uri']
        widgets = {
            'redirect_uri': Textarea(),
        }


class DeleteOauthAppForm(Form):
    pass
