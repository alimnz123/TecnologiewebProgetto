from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Interno, Lettera_Convocazione, Verbale, DocumentiPalazzo, Fornitore, Spesa


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    interno=forms.ChoiceField(required=True, choices=Interno)

    class Meta:
        model = User
        fields = ["username", "email", "first_name",
                  "last_name", "password1", "password2"]


class InternoForm(forms.ModelForm):
    class Meta:
        model = Interno
        fields = ["condomino", "numero_interno", "palazzina", 
                  "millesimi_generali", "millesimi_scala", "in_affitto", "mappali"]


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
    class Meta:
        model = DocumentiPalazzo
        fields = ["data", "descrizione", "file_documento"]

class FornitoreForm(forms.ModelForm):
    class Meta:
        model = Fornitore
        fields = ["nome", "contratto", "indirizzo",
                  "ragione_sociale", "partita_iva", "cf", "iban"]
        
class SpesaForm(forms.ModelForm):
    class Meta:
        model = Spesa
        fields = ["data", "fornitore", "tipologia",
                  "descrizione", "assegnatario", "importo"]
