from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    first_name = forms.CharField(label= "Imie")
    last_name = forms.CharField(label="Nazwisko")
    username = forms.CharField(label="Login (email)")
    # password = forms.CharField(label="Hasło")
    # password2 = forms.CharField(label="Powtórz hasło")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
        # field_classes = {'username': UsernameField}
