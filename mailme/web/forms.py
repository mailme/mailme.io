from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy, ugettext as _

from mailme.core.models import User


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label=ugettext_lazy('Your email address'),
        widget=forms.TextInput({'placeholder': 'support@mailme.io'})
    )

    def clean_email(self):
        """
        Validates if the required field `email` contains
        a non existing mail address.
        """
        exists = User.objects.filter(email=self.cleaned_data['email']).exists()
        if exists:
            raise forms.ValidationError(mark_safe(
                _('The given email address is already in use. '
                  '<a href="{link}">Forgot your password?</a>'.format(link=''))
            ))
        return self.cleaned_data['email']
