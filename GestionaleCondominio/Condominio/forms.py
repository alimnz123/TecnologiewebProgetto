from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Interno, Lettera_Convocazione, Verbale, DocumentiPalazzo, Fornitore, Spesa, Rata


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, label="Nome")
    last_name = forms.CharField(required=True, label="Cognome")
    interno=forms.ChoiceField(required=True, choices=Interno, label="Interno")

    class Meta:
        model = User
        fields = ["username", "email", "first_name",
                  "last_name", "password1", "password2"]


class InternoForm(forms.ModelForm):
    class Meta:
        model = Interno
        fields = ["condomino", "numero_interno", "palazzina", 
                  "millesimi_generali", "millesimi_scala", "in_affitto"]


class LettereConvocazioneForm(forms.ModelForm):
    class Meta:
        model = Lettera_Convocazione
        fields = ["data", "descrizione", "convocazione_documento"]


class VerbaleForm(forms.ModelForm):
    class Meta:
        model = Verbale
        fields = ["data", "descrizione",
                  "documento", "lettera_accompagnatoria"]
        
class DocumentiPalazzoForm(forms.ModelForm):
    data= forms.SelectDateWidget(empty_label="Nothing")
    class Meta:
        model = DocumentiPalazzo
        fields = ["data", "descrizione", "file_documento"]

class FornitoreForm(forms.ModelForm):
    class Meta:
        model = Fornitore
        fields = ["nome", "contratto", "indirizzo",
                  "ragione_sociale", "partita_iva", "cf", "iban"]
        
class SpesaForm(forms.ModelForm):
    data=forms.DateField(
        widget=forms.DateInput(
            attrs = {
            'class': 'form-control',
            'type' : 'date'
            }
        )
    )
    class Meta:
        model = Spesa
        fields = ["data", "fornitore", "tipologia",
                  "descrizione", "assegnatario", "importo"]
        
class RataForm(forms.ModelForm):
    data_scadenza=forms.DateField(
        widget=forms.DateInput(
            attrs = {
            'class': 'form-control',
            'type' : 'date'
            }
        )
    )
    class Meta:
        model = Rata
        fields = ["assegnatario", "data_scadenza", "descrizione",
                  "importo", "pagata", "file_pagamento"]

class EditUserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ["username", "email", "first_name",
                  "last_name"]
        labels = {'email': 'Email', 'first_name': 'Nome', 'last_name':'Cognome'}

class EditAdminProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = '__all__'
        labels = {'email': 'Email'}