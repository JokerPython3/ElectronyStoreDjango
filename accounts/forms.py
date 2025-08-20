from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegisterForms(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords error.")
        return cleaned_data

class LoginForms(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)