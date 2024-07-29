from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Interno

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

class InternoForm(forms.ModelForm):
    class Meta:
        model = Interno 
        fields=["condomino","palazzina", "numero", "millesimi_generali", "millesimi_scala", "in_affitto", "mappali"]