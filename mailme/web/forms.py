from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='Your email address',
        widget=forms.TextInput({'placeholder': 'support@mailme.io'})
    )
