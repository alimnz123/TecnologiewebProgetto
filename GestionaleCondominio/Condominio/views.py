from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .forms import RegisterForm, InternoForm, LettereConvocazioneForm, VerbaleForm, DocumentiPalazzoForm, FornitoreForm, SpesaForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import *
from datetime import datetime

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

    return render(request, 'registration/sign_up.html', {"form": form})


def my_login(request):
    pass

def logout_view(request):
    logout(request)
    redirect('/logout')

def dashboard(request):
    pass

#HOMEPAGE
@login_required(login_url="/login")
def homepage(request):
    return render(request, 'Condominio_main/homepage.html')

#Classe DeleteView per una generica entità
class DeleteEntitaView(DeleteView):
    template_name="Condominio_main/cancella_elemento.html"

    def get_context_data(self, **kwargs):
        ctx=super().get_context_data()
        if self.model == Interno:
            entita="Interno"
        if self.model == Spesa:
            entita="Spesa"
        if self.model == DocumentiPalazzo:
            entita="DocumentiPalazzo"
        if self.model == Verbale:
            entita="Verbale"
        if self.model == Lettera_Convocazione:
            entita="LetteraConvocazione"
        if self.model == Fornitore:
            entita="Fornitore"
        ctx["entita"]=entita
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

@login_required(login_url="/login")
def bacheca(request):
    verbali=Verbale.objects.all()
    lettere=Lettera_Convocazione.objects.all()

    if request.method == "POST":
        lettera_id = request.POST.get("lettera-id")
        print(lettera_id)
        lettera=Lettera_Convocazione.objects.filter(id=lettera_id).first()
        if lettera and (lettera.author == request.user or request.user.has_perm("main.delete_lettera")):
            lettera.delete()

    if request.method == "POST":
        verbale_id = request.POST.get("verbale-id")
        print(verbale_id)
        verbale=Verbale.objects.filter(id=verbale_id).first()
        if verbale and (verbale.author == request.user or request.user.has_perm("main.delete_verbale")):
            verbale.delete()

    return render(request, 'Condominio_main/bacheca.html', {"verbali":verbali, "lettere di convocazione": lettere})

class DeleteVerbaleView(DeleteEntitaView):
    model=Verbale
class DeleteLetteraConvocazioneView(DeleteEntitaView):
    model=Lettera_Convocazione

@login_required(login_url="/login")
def documenti_palazzo(request):
    documenti=DocumentiPalazzo.objects.all()

    if request.method == "POST":
        documento_id = request.POST.get("documento-id")
        print(documento_id)
        documento=DocumentiPalazzo.objects.filter(id=documento_id).first()
        if documento and (request.user.has_perm("main.delete_documento")):
            documento.delete()

    return render(request, 'Condominio_main/documenti_palazzo.html', {"documenti":documenti})

class DeleteDocumentiPalazzoView(DeleteEntitaView):
    model=DocumentiPalazzo

@login_required(login_url="/login")
@permission_required("main.add_lettera", login_url="/login", raise_exception=True)
def create_lettera(request):
    if request.method == 'POST':
        form = LettereConvocazioneForm(request.POST)
        if form.is_valid():
            lettera = form.save(commit=False)
            lettera.author = request.user
            lettera.save()
            return redirect("/home")
    else:
        form = LettereConvocazioneForm()

    return render(request, 'Condominio_main/create_lettera.html', {"form": form})    

@login_required(login_url="/login")
@permission_required("main.add_lettera", login_url="/login", raise_exception=True)
def create_verbale(request):
    if request.method == 'POST':
        form = VerbaleForm(request.POST)
        if form.is_valid():
            verbale = form.save(commit=False)
            verbale.author = request.user
            verbale.save()
            return redirect("/home")
    else:
        form = LettereConvocazioneForm()

    return render(request, 'Condominio_main/create_verbale.html', {"form": form})    


@login_required(login_url="/login")
@permission_required("main.add_documento", login_url="/login", raise_exception=True)
def create_documento(request):
    if request.method == 'POST':
        form = DocumentiPalazzoForm(request.POST)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.author = request.user
            documento.save()
            #faccio partire una notifica
            Notification.objects.create(text="New answer!")
            return redirect("/home")
    else:
        form = DocumentiPalazzoForm()

    return render(request, 'Condominio_main/create_documento.html', {"form": form})


#views related to Fornitori and Spese

@login_required(login_url="/login")
def fornitori(request):
    fornitori=Fornitore.objects.all()

    if request.method == "POST":
        fornitore_id = request.POST.get("fornitore-id")
        print(fornitore_id)
        fornitore=Fornitore.objects.filter(id=fornitore_id).first()
        if fornitore and (fornitore.author == request.user or request.user.has_perm("main.delete_fornitore")):
            fornitore.delete()
            
    return render(request, 'Condominio_main/fornitori.html', {"fornitori":fornitori})

@login_required(login_url="/login")
@permission_required("main.add_fornitore", login_url="/login", raise_exception=True)
def create_fornitore(request):
    if request.method == 'POST':
        form = FornitoreForm(request.POST)
        if form.is_valid():
            fornitore = form.save(commit=False)
            fornitore.author = request.user
            fornitore.save()
            return redirect("/fornitori")
    else:
        form = FornitoreForm()

    return render(request, 'Condominio_main/create_fornitore.html', {"form": form})

class DeleteFornitoreView(DeleteEntitaView):
    model=Fornitore

class UpdateFornitoreView(UpdateView):
    model = Fornitore
    fields = "__all__"
    template_name = "Condominio_main/edit_fornitore.html"
    
    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("fornitori", kwargs = {'pk': pk})

@login_required(login_url="/login")
def spesa(request):
    spese=Spesa.objects.all()
    
    """ if request.method == "POST":
        spesa_id = request.POST.get("spesa-id")
        print(spesa_id)
        spesa=Spesa.objects.filter(id=spesa_id).first()
        if spesa and (request.user.has_perm("main.delete_spesa")):
            spesa.delete() """
            
    return render(request, 'Condominio_main/spese.html', {"spese":spese})

@login_required(login_url="/login")
@permission_required("main.add_spesa", login_url="/login", raise_exception=True)
def create_spesa(request):
    if request.method == 'POST':
        form = SpesaForm(request.POST)
        if form.is_valid():
            spesa = form.save(commit=False)
            spesa.author = request.user
            spesa.save()
            return redirect("/spesa")
    else:
        form = SpesaForm()

    return render(request, 'Condominio_main/create_spesa.html', {"form": form})

class UpdateSpesaView(UpdateView):
    model = Spesa
    fields='__all__'
    template_name = "Condominio_main/edit_spesa.html"
    

    def get_success_url(self):
        pk = self.get_context_data()["object"].id
        return reverse("spesa",kwargs={'pk': pk})
    
class DeleteSpesaView(DeleteEntitaView):
    model=Spesa

#VIEW INTERNO CON IL RISEPTTIVO OCCUPANTE
    #view che permette di visionare tutti i consomini e in quali interni si trovano
@login_required(login_url="/login")
def interno(request):
    interni=Interno.objects.all()

    if request.method == "POST":
        interno_id = request.POST.get("interno-id")
        print(interno_id)
        interno=Interno.objects.filter(id=interno_id).first()
        if interno and (request.user.has_perm("main.delete_interno")):
            interno.delete()
            
    return render(request, 'Condominio_main/interni.html', {"interni":interni})

class UpdateInternoView(UpdateView):
    model = Interno
    fields = "__all__"
    template_name = "Condominio_main/edit_interno.html"
    
    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("interni", kwargs = {'pk': pk})
    
@login_required(login_url="/login")
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
    model=Interno


#RIPARTO PREVENTIVO
GEN = "SPESA_GENERALE"
class RipartoPreventivoView(ListView):
    model=Spesa
    template_name="Condominio_main/riparto_preventivo.html"
    def spese_generali_totale(self):
        current_date=datetime.now()
        current_year=current_date.year
        spese_generali=Spesa.objects.filter(tipologia__eq=GEN, data__eq=current_year)
        totale_spese=0
        for spesa in spese_generali:
            totale_spese += spesa.importo
            return totale_spese
        return render({"totale_generali": totale_spese})
    
#RIPARTO PREVENTIVO
STRAORDINARIE_EDIFICI = "SPESA_STRAORDINARIA_EDIFICIO"
class RipartoConsuntivoView(ListView):
    model=Spesa
    template_name="Condominio_main/riparto_consuntivo.html"

    def get_numero_interno(self):
        interni=Interno.objects.all()
        return interni
    
    def totale_spese_straordinarie_edifici(self):
        interni=Interno.objects.all()
        current_date=datetime.now()
        current_year=current_date.year
        spese_straordinarie_edifici=Spesa.objects.filter(tipologia=STRAORDINARIE_EDIFICI, data__year=current_year)
        totale_spese=0
        for spesa in spese_straordinarie_edifici:
            totale_spese += spesa.importo
            return totale_spese
        
    def totale_spese_straordinarie_scale(self):
        pass
    
    def totale_spese_straordinarie_antenne(self):
        pass
    
    def totale_spese_diverse(self):
        pass
    
    def totale_spese_esercizio_precedente(self):
        pass

    def totale_saldo_esercizio_precedente(self):
        pass

    def totale_complessivo(self):
        pass
    
    def totale_versamenti_anno_precedente(self):
        pass
        
    def saldi_esercizio(self):
        pass

    #da continuare da manutenzione ordinaria in poi

    
#NOTIFICATION SYSTEM
#view che mette in lista tutte le notifiche

@login_required(login_url="/login")
def notifiche(request):
    notifiche=Notification.objects.all()

    if request.method == "POST":
        notifica_id = request.POST.get("notifica-id")
        print(notifica_id)
        notifica=Notification.objects.filter(id=notifica_id).first()
        if notifica and (request.user.has_perm("main.delete_notifica")):
            notifica.delete()
            
    return render(request, 'Condominio_main/notifiche.html', {"notifiche":notifiche})
class NotificationListView(ListView):
    model = Notification

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-timestamp")


