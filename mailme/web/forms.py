from django import forms
from django.contrib.auth.forms import (
    UserChangeForm as AuthUserChangeForm,
    UserCreationForm as AuthUserCreationForm
)
from django.core import validators
from django.utils.translation import ugettext_lazy as _

from mailme.core.models import User


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        validators=[validators.MinLengthValidator(5)],
        help_text=_(
            'Your password should not contain your username. '
            'Please use special signs too.'
        )
    )
    password2 = forms.CharField(
        label=_('Password confirm'),
        widget=forms.PasswordInput,
        validators=[validators.MinLengthValidator(5)]
    )

    error_messages = {
        'username_in_use': _('The username is already in use.'),
        'password_mismatch': _('Passwords don\'t match.')
    }

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for field in ('username', 'email', 'password1', 'password2'):
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                self.error_messages['username_in_use'], code='username_in_use')

        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch')
        return password2


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={'placeholder': _('Username')}))
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'placeholder': _('Password')}))

    error_messages = {
        'authentication_mismatch': _(
            u'Please enter a correct username and password. '
            u'Note that the password is case-sensitive.'
        )
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = self.authenticate(username, password)

        if not user:
            raise forms.ValidationError(
                self.error_messages['authentication_mismatch'],
                code='authentication_mismatch')

        self.cleaned_data['user'] = user
        return self.cleaned_data

    def authenticate(self, username, password):
        if not username or not password:
            return

        try:
            user = User.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
