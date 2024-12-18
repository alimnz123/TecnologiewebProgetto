from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.urls import reverse_lazy, reverse
from .forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate, views
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import *
from datetime import datetime
from django.db.models import Case, Value, When, Q
from django.contrib import messages

# Create your views here.


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # i want to create a new user
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')

    else:
        form = RegisterForm()

    return render(request, "registration/sign_up.html", {"form": form})


def my_login(request):
    return render(request, "registration/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login")

def dashboard(request):
    pass

def success(request):
    return render(request, 'Condominio_main/success.html')

def handle_uploaded_file(f):
    with open("some/file/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# PROFILO UTENTE
def profilo_utente(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user.is_staff == True:
                fm = EditAdminProfileForm(request.POST, instance=request.user)
                utenti = User.objects.all()
            else:
                fm = EditUserProfileForm(request.POST, instance=request.user)
                utenti = None
            if fm.is_valid():
                messages.success(request, 'Profilo aggiornato')
                fm.save()
        else:
            if request.user.is_staff == True:
                fm = EditAdminProfileForm(instance=request.user)
                utenti = User.objects.all()
            else:
                fm = EditUserProfileForm(instance=request.user)
                utenti = None
        return render(request, 'Condominio_main/profilo.html',
                      {'Nome': request.user.username, 'form': fm, 'utenti': utenti})
    else:
        return redirect('/home')

# HOMEPAGE
@login_required(login_url='login')
def homepage(request):
    condominio = Condominio.objects.first()
    return render(request, 'Condominio_main/homepage.html', {"condominio": condominio})

# Classe DeleteView per una generica entità
class DeleteEntitaView(DeleteView):
    template_name = "Condominio_main/cancella_elemento.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        if self.model == Interno:
            entita = "Interno"
        if self.model == Spesa:
            entita = "Spesa"
        if self.model == DocumentiPalazzo:
            entita = "DocumentiPalazzo"
        if self.model == Verbale:
            entita = "Verbale"
        if self.model == Lettera_Convocazione:
            entita = "LetteraConvocazione"
        if self.model == Fornitore:
            entita = "Fornitore"
        ctx["entita"] = entita
        return ctx

    def get_success_url(self):
        if self.model == Interno:
            return reverse("interni")
        if self.model == Spesa:
            return reverse("spesa")
        if self.model == DocumentiPalazzo:
            return reverse("documenti_palazzo")
        if self.model == Verbale:
            return reverse("bacheca")
        if self.model == Lettera_Convocazione:
            return reverse("bacheca")
        if self.model == Fornitore:
            return reverse("fornitori")
        return super().get_success_url()


@login_required(login_url='login')
def bacheca(request):
    verbali = Verbale.objects.all()
    lettere = Lettera_Convocazione.objects.all()

    if request.method == "POST":
        lettera_id = request.POST.get("lettera-id")
        print(lettera_id)
        lettera = Lettera_Convocazione.objects.filter(id=lettera_id).first()
        if lettera and (request.user.has_perm("main.delete_lettera")):
            lettera.delete()

    if request.method == "POST":
        verbale_id = request.POST.get("verbale-id")
        print(verbale_id)
        verbale = Verbale.objects.filter(id=verbale_id).first()
        if verbale and (request.user.has_perm("main.delete_verbale")):
            verbale.delete()

    return render(request, 'Condominio_main/bacheca.html', {"verbali": verbali, "lettere": lettere})


class DeleteVerbaleView(DeleteEntitaView):
    model = Verbale


class DeleteLetteraConvocazioneView(DeleteEntitaView):
    model = Lettera_Convocazione


@login_required(login_url='login')
def documenti_palazzo(request):
    documenti = DocumentiPalazzo.objects.all()

    if request.method == "POST":
        documento_id = request.POST.get("documento-id")
        print(documento_id)
        documento = DocumentiPalazzo.objects.filter(id=documento_id).first()
        if documento and (request.user.has_perm("main.delete_documento")):
            documento.delete()

    return render(request, 'Condominio_main/documenti_palazzo.html', {"documenti": documenti})


class DeleteDocumentiPalazzoView(DeleteEntitaView):
    model = DocumentiPalazzo


@login_required(login_url='login')
@permission_required("main.add_lettera", login_url='login', raise_exception=True)
def create_lettera(request):
    if request.method == "POST":
        form = LettereConvocazioneForm(request.POST, request.FILES)
        if form.is_valid():
            let_data = form.cleaned_data['data']
            let_descrizione = form.cleaned_data['descrizione']
            let_convocazione_documento = form.cleaned_data['convocazione_documento']

            let = Lettera_Convocazione.objects.create(
                data=let_data,
                descrizione=let_descrizione,
                convocazione_documento=let_convocazione_documento
            )

            let.save()
            form.save()

            return HttpResponseRedirect("/bacheca")
    form = LettereConvocazioneForm()
    return render(request, 'Condominio_main/create_lettera.html', {"form": form})


@login_required(login_url='login')
@permission_required("main.add_lettera", login_url='login', raise_exception=True)
def create_verbale(request):
    if request.method == "POST":
        form = VerbaleForm(request.POST, request.FILES)
        if form.is_valid():
            verb_data = form.cleaned_data['data']
            verb_descrizione = form.cleaned_data['descrizione']
            verb_documento = form.cleaned_data['documento']
            verb_lettera_accompagnatoria = form.cleaned_data['lettera_accompagnatoria']

            verb = Verbale.objects.create(
                data=verb_data,
                descrizione=verb_descrizione,
                documento=verb_documento,
                lettera_accompagnatoria=verb_lettera_accompagnatoria
            )

            verb.save()
            form.save()

            return HttpResponseRedirect("/bacheca")
    form = VerbaleForm()
    return render(request, 'Condominio_main/create_verbale.html', {"form": form})


@login_required(login_url='login')
@permission_required("main.add_documento", login_url='login', raise_exception=True)
def create_documento(request):
    if request.method == "POST":
        form = DocumentiPalazzoForm(request.POST, request.FILES)
        if form.is_valid():
            pal_data = form.cleaned_data['data']
            pal_descrizione = form.cleaned_data['descrizione']
            pal_file_documento = form.cleaned_data['file_documento']

            pal = DocumentiPalazzo.objects.create(
                data=pal_data,
                descrizione=pal_descrizione,
                file_documento=pal_file_documento
            )

            pal.save()
            form.save()

            return HttpResponseRedirect("/bacheca")
    form = DocumentiPalazzoForm()
    return render(request, 'Condominio_main/create_documento.html', {"form": form})

# views related to Fornitori and Spese


@login_required(login_url='login')
def fornitori(request):
    fornitori = Fornitore.objects.all()

    if request.method == "POST":
        fornitore_id = request.POST.get("fornitore-id")
        print(fornitore_id)
        fornitore = Fornitore.objects.filter(id=fornitore_id).first()
        if fornitore and (request.user.has_perm("main.delete_fornitore")):
            fornitore.delete()

    return render(request, 'Condominio_main/fornitori.html', {"fornitori": fornitori})


@login_required(login_url='login')
@permission_required("main.add_fornitore", login_url='login', raise_exception=True)
def create_fornitore(request):
    if request.method == "POST":
        form = FornitoreForm(request.POST, request.FILES)
        if form.is_valid():
            forn_nome = form.cleaned_data['nome']
            forn_contratto = form.cleaned_data['contratto']
            forn_indirizzo = form.cleaned_data['indirizzo']
            forn_ragione_sociale = form.cleaned_data['ragione_sociale']
            forn_partita_iva = form.cleaned_data['partita_iva']
            forn_cf = form.cleaned_data['cf']
            forn_iban = form.cleaned_data['iban']

            forn = Fornitore.objects.create(
                nome=forn_nome,
                contratto=forn_contratto,
                indirizzo=forn_indirizzo,
                ragione_sociale=forn_ragione_sociale,
                partita_iva=forn_partita_iva,
                cf=forn_cf,
                iban=forn_iban
            )

            forn.save()
            form.save()

            return HttpResponseRedirect("/fornitori")
    form = FornitoreForm()
    return render(request, 'Condominio_main/create_fornitore.html', {"form": form})


class DeleteFornitoreView(DeleteEntitaView):
    model = Fornitore


def update_fornitore(request, nome):
    fornitore = get_object_or_404(Fornitore, nome = nome)
    form = FornitoreForm(request.POST or None, instance = fornitore)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/fornitori")
    return render(request, 'Condominio_main/edit_fornitore.html', {'form': form})


@login_required(login_url='login')
def spesa(request):
    spese = Spesa.objects.all()

    """ if request.method == "POST":
        spesa_id = request.POST.get("spesa-id")
        print(spesa_id)
        spesa=Spesa.objects.filter(id=spesa_id).first()
        if spesa and (request.user.has_perm("main.delete_spesa")):
            spesa.delete() """

    return render(request, 'Condominio_main/spese.html', {"spese": spese})


@login_required(login_url='login')
@permission_required("main.add_spesa", login_url='login', raise_exception=True)
def create_spesa(request):
    if request.method == "POST":
        form = SpesaForm(request.POST)
        if form.is_valid():
            spe_fornitore = form.cleaned_data['fornitore']
            spe_data = form.cleaned_data['data']
            spe_tipologia = form.cleaned_data['tipologia']
            spe_descrizione = form.cleaned_data['descrizione']
            spe_assegnatario = form.cleaned_data['assegnatario']
            spe_importo = form.cleaned_data['importo']
            
            spe = Spesa.objects.create(
                fornitore=spe_fornitore,
                data=spe_data,
                tipologia=spe_tipologia,
                descrizione=spe_descrizione,
                assegnatario=spe_assegnatario,
                importo=spe_importo
            )

            spe.save()
            form.save()

            return HttpResponseRedirect("/spesa")
    form = SpesaForm()
    return render(request, 'Condominio_main/create_spesa.html', {"form": form})



def update_spesa(request, fornitore):
    spesa = get_object_or_404(Spesa, fornitore = fornitore)
    form = SpesaForm(request.POST or None, instance = spesa)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/spesa")
    return render(request, 'Condominio_main/edit_spesa.html', {'form': form})


class DeleteSpesaView(DeleteEntitaView):
    model = Spesa

# VIEW INTERNO CON IL RISEPTTIVO OCCUPANTE
    # view che permette di visionare tutti i consomini e in quali interni si trovano


@login_required(login_url='login')
def interno(request):
    interni = Interno.objects.all()

    if request.method == "POST":
        interno_id = request.POST.get("interno-id")
        print(interno_id)
        interno = Interno.objects.filter(id=interno_id).first()
        if interno and (request.user.has_perm("main.delete_interno")):
            interno.delete()

    return render(request, 'Condominio_main/interni.html', {"interni": interni})


class UpdateInternoView(UpdateView):
    model = Interno
    fields = "__all__"
    template_name = "Condominio_main/edit_interno.html"

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("interni", kwargs={'pk': pk})


@login_required(login_url='login')
def create_interno(request):
    if request.method == 'POST':
        form = InternoForm(request.POST)
        if form.is_valid():
            interno = form.save(commit=False)
            interno.author = request.user
            interno.save()
            return redirect("interni")
    else:
        form = InternoForm()

    return render(request, 'Condominio_main/create_interno.html', {"form": form})


class DeleteInternoView(DeleteEntitaView):
    model = Interno


# RIPARTO CONSUNTIVO
@login_required(login_url='login')
def RipartoConsuntivo(request):
    interni = Interno.objects.all()

    # Elementi utili
    current_date = datetime.now()
    anno_precedente = current_date.year - 1

    ctx = {"interni": interni, "anno_precedente": anno_precedente}

    return render(request, "Condominio_main/riparto_consuntivo.html", ctx)


@login_required(login_url='login')
def RipartoPreventivo(request):
    interni = Interno.objects.all()

    # spese straordinarie edifici
    current_date = datetime.now()
    anno_successivo = current_date.year + 1

    ctx = {"interni": interni, "anno_successivo": anno_successivo}
    return render(request, "Condominio_main/riparto_preventivo.html", ctx)
