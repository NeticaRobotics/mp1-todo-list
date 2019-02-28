from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    ocupation = forms.CharField(label="Ocupation", max_length=60, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'ocupation', 'password1', 'password2', )
