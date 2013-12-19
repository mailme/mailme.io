from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField(label='Your email address')
