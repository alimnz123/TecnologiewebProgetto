from django.shortcuts import render, redirect, HttpResponseRedirect
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
from notifications.signals import notify
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

    return render(request, 'registration/sign_up.html', {"form": form})


def my_login(request):
    pass

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def dashboard(request):
    pass

#PROFILO UTENTE
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

#HOMEPAGE
@login_required(login_url="/login")
def homepage(request):
    condominio=Condominio.objects.first()
    return render(request, 'Condominio_main/homepage.html', {"condominio":condominio})

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
        if lettera and (request.user.has_perm("main.delete_lettera")):
            lettera.delete()

    if request.method == "POST":
        verbale_id = request.POST.get("verbale-id")
        print(verbale_id)
        verbale=Verbale.objects.filter(id=verbale_id).first()
        if verbale and (request.user.has_perm("main.delete_verbale")):
            verbale.delete()
    
    return render(request, 'Condominio_main/bacheca.html', {"verbali":verbali, "lettere": lettere})

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
            messages.success(request, "Profile details updated.")
            #notifica se viene aggiunto un nuovo verbale
            notify.send(sender=request.user, recipient=request.user, verb="Nuova Lettera di Convocazione", action_objects=form)
            return redirect("/bacheca")
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
            #notifica
            notify.send(sender=request.user, recipient=request.user, verb="Nuovo Verbale", action_objects=form)
            return redirect("/bacheca")
    else:
        form = VerbaleForm()

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
            
            return redirect("/documenti_palazzo")
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
        if fornitore and (request.user.has_perm("main.delete_fornitore")):
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


#RIPARTO CONSUNTIVO
@login_required(login_url="/login")
def RipartoConsuntivo(request):
    interni=Interno.objects.all()
    
    #spese straordinarie edifici
    current_date = datetime.now()
    current_year = current_date.year
    anno_precedente=current_date.year - 1

    spese_straordinarie_edifici=Spesa.objects.filter(Q(tipologia="Spesa Straordinaria Edificio") & Q(data__year=current_year))

    totale_spese_straordinarie_edifici = 0
    for spesa in spese_straordinarie_edifici:
        totale_spese_straordinarie_edifici += spesa.importo
    
    #spese straordinarie scale
    spese_straordinarie_scale=Spesa.objects.filter(Q(tipologia="Spesa Straordinaria Scale") & Q(data__year=current_year))

    totale_spese_straordinarie_scale = 0
    for spesa in spese_straordinarie_scale:
        totale_spese_straordinarie_scale += spesa.importo

    #spese straordinarie antenne
    spese_straordinarie_antenne=Spesa.objects.filter(Q(tipologia="Spesa Straordinaria Antenne") & Q(data__year=current_year))

    totale_spese_straordinarie_antenne = 0
    for spesa in spese_straordinarie_antenne:
        totale_spese_straordinarie_antenne += spesa.importo

    #spese diverse
    spese_diverse=Spesa.objects.filter(Q(tipologia="Spese Diverse") & Q(data__year=current_year))

    totale_spese_diverse = 0
    for spesa in spese_diverse:
        totale_spese_diverse += spesa.importo

    #totale esercizio
    spese_totali=Spesa.objects.filter(Q(data__year=current_year))

    totale_esercizio = 0
    for spesa in spese_totali:
        totale_esercizio += spesa.importo

    #saldo esercizio precedente
    saldo_esercizio_precedente = 0  #trova un modo per salvare le rate versate nell'anno precedente

    #totale complessivo
    totale_complessivo = totale_esercizio - saldo_esercizio_precedente

    #versamento anno trascorso, sono le rate già versate nell'anno appena trascorso
        #query seleziono le rate pagate nell'anno corrente e sommo gli importi
    versamento_anno_trascorso = 0

    #saldi di esercizio
    saldi_esercizio=totale_complessivo-versamento_anno_trascorso

    #manutenzione ordinaria scale
    spese_ordinarie_scale=Spesa.objects.filter(Q(tipologia="Manutenzione Ordinaria Scala") & Q(data__year=current_year))

    totale_ordinarie_scale = 0
    for spesa in spese_ordinarie_scale:
        totale_ordinarie_scale += spesa.importo
    
    #manutenzione ordinaria 
    spese_ordinarie=Spesa.objects.filter(Q(tipologia="Manutenzione Ordinaria") & Q(data__year=current_year))

    totale_ordinarie = 0
    for spesa in spese_ordinarie:
        totale_ordinarie += spesa.importo

    #manutenzione ordinaria aree comuni 
    spese_ordinarie_comuni=Spesa.objects.filter(Q(tipologia="Manutenzione Ordinaria") & Q(data__year=current_year))

    totale_ordinarie_comuni = 0
    for spesa in spese_ordinarie_comuni:
        totale_ordinarie_comuni += spesa.importo

    #totale manutenzioni ordinarie
    totale_utente_manutenzioni_ordinarie=totale_ordinarie_comuni+totale_ordinarie+totale_ordinarie_scale
        
    #spese gnerali
    spese_generali=Spesa.objects.filter(Q(tipologia="Spese Generali") & Q(data__year=current_year))

    totale_generali = 0
    for spesa in spese_generali:
        totale_generali += spesa.importo

    #spese gnerali
    spese_straordinarie=Spesa.objects.filter(Q(tipologia="Spese Straordinarie") & Q(data__year=current_year))

    totale_straordinarie = 0
    for spesa in spese_straordinarie:
        totale_straordinarie += spesa.importo

    return render(request, "Condominio_main/riparto_consuntivo.html", {"interni":interni, "anno_precedente": anno_precedente, "totale_spese_straordinarie_edifici":totale_spese_straordinarie_edifici, "totale_spese_straordinarie_scale":totale_spese_straordinarie_scale,
                                                                       "totale_spese_straordinarie_antenne":totale_spese_straordinarie_antenne, "totale_spese_diverse":totale_spese_diverse, "totale_esercizio": totale_esercizio, "saldo_esercizio_precedente":saldo_esercizio_precedente,
                                                                       "totale_complessivo":totale_complessivo, "versamento_anno_trascorso":versamento_anno_trascorso, "saldi_esercizio":saldi_esercizio, "totale_ordinarie_scale":totale_ordinarie_scale, "totale_ordinarie":totale_ordinarie,
                                                                       "totale_ordinarie_comuni":totale_ordinarie_comuni, "totale_utente_manutenzioni_ordinarie":totale_utente_manutenzioni_ordinarie, "totale_generali":totale_generali, "totale_straordinarie": totale_straordinarie})

@login_required(login_url="/login")
def RipartoPreventivo(request):
    interni=Interno.objects.all()
    
    #spese straordinarie edifici
    current_date = datetime.now()
    current_year = current_date.year
    anno_precedente = current_date.year - 1

    spese_straordinarie_edifici=Spesa.objects.filter(Q(tipologia="Spesa Straordinaria Edificio") & Q(data__year=current_year-1))

    totale_spese_straordinarie_edifici = 0
    for spesa in spese_straordinarie_edifici:
        totale_spese_straordinarie_edifici += spesa.importo
    totale_spese_straordinarie_edifici += (totale_spese_straordinarie_edifici*0.10)

    #spese straordinarie scale
    spese_straordinarie_scale=Spesa.objects.filter(Q(tipologia="Spesa Straordinaria Scale") & Q(data__year=current_year))

    totale_spese_straordinarie_scale = 0
    for spesa in spese_straordinarie_scale:
        totale_spese_straordinarie_scale += spesa.importo

    #spese straordinarie antenne
    spese_straordinarie_antenne=Spesa.objects.filter(Q(tipologia="Spesa Straordinaria Antenne") & Q(data__year=current_year))

    totale_spese_straordinarie_antenne = 0
    for spesa in spese_straordinarie_antenne:
        totale_spese_straordinarie_antenne += spesa.importo

    #spese diverse
    spese_diverse=Spesa.objects.filter(Q(tipologia="Spese Diverse") & Q(data__year=current_year))

    totale_spese_diverse = 0
    for spesa in spese_diverse:
        totale_spese_diverse += spesa.importo

    #totale esercizio
    spese_totali=Spesa.objects.filter(Q(data__year=current_year-1))

    totale_esercizio = 0
    for spesa in spese_totali:
        totale_esercizio += spesa.importo

    totale_esercizio+=(totale_esercizio*0.10)  #il riparto preventivo REGOLAMENTIAMO che da previsione preveda un aumento del 10% ogni anno

    #saldo esercizio precedente
    saldo_esercizio_precedente = 0  #trova un modo per salvare le rate versate nell'anno appena passato

    #totale complessivo
    totale_complessivo = totale_esercizio - saldo_esercizio_precedente

    #versamento anno trascorso, sono le rate già versate nell'anno appena trascorso
        #query seleziono le rate pagate nell'anno corrente e sommo gli importi
    versamento_anno_trascorso = 0

    #saldi di esercizio
    saldi_esercizio=totale_complessivo-versamento_anno_trascorso

    #manutenzione ordinaria scale
    spese_ordinarie_scale=Spesa.objects.filter(Q(tipologia="Manutenzione Ordinaria Scala") & Q(data__year=current_year-1))

    totale_ordinarie_scale = 0
    for spesa in spese_ordinarie_scale:
        totale_ordinarie_scale += spesa.importo
    totale_ordinarie_scale += (totale_ordinarie_scale*0.10) #il riparto preventivo REGOLAMENTIAMO che da previsione preveda un aumento del 10% ogni anno
    
    #manutenzione ordinaria 
    spese_ordinarie=Spesa.objects.filter(Q(tipologia="Manutenzione Ordinaria") & Q(data__year=current_year-1))

    totale_ordinarie = 0
    for spesa in spese_ordinarie:
        totale_ordinarie += spesa.importo
    totale_ordinarie+=(totale_ordinarie*0.10) #il riparto preventivo REGOLAMENTIAMO che da previsione preveda un aumento del 10% ogni anno

    #manutenzione ordinaria aree comuni 
    spese_ordinarie_comuni=Spesa.objects.filter(Q(tipologia="Manutenzione Ordinaria") & Q(data__year=current_year-1))

    totale_ordinarie_comuni = 0
    for spesa in spese_ordinarie_comuni:
        totale_ordinarie_comuni += spesa.importo

    #totale manutenzioni ordinarie
    totale_utente_manutenzioni_ordinarie=(totale_ordinarie_comuni+totale_ordinarie+totale_ordinarie_scale)*0.10
        
    #spese gnerali
    spese_generali=Spesa.objects.filter(Q(tipologia="Spese Generali") & Q(data__year=current_year - 1)) #leggo le spese generali dell'anno scorso

    totale_generali = 0
    for spesa in spese_generali:
        totale_generali += spesa.importo
    totale_generali += (totale_generali*0.10) #il riparto preventivo REGOLAMENTIAMO che da previsione preveda un aumento del 10% ogni anno

    #spese straordinarie
    spese_straordinarie=Spesa.objects.filter(Q(tipologia="Spese Straordinarie") & Q(data__year=current_year-1))

    totale_straordinarie = 0
    for spesa in spese_straordinarie:
        totale_straordinarie += spesa.importo
    totale_straordinarie+=(totale_straordinarie*0.10) #il riparto preventivo REGOLAMENTIAMO che da previsione preveda un aumento del 10% ogni anno


    return render(request, "Condominio_main/riparto_preventivo.html", {"interni":interni, "anno_precedente": anno_precedente, "totale_spese_straordinarie_edifici":totale_spese_straordinarie_edifici, "totale_spese_straordinarie_scale":totale_spese_straordinarie_scale,
                                                                       "totale_spese_straordinarie_antenne":totale_spese_straordinarie_antenne, "totale_spese_diverse":totale_spese_diverse, "totale_esercizio": totale_esercizio, "saldo_esercizio_precedente":saldo_esercizio_precedente,
                                                                       "totale_complessivo":totale_complessivo, "versamento_anno_trascorso":versamento_anno_trascorso, "saldi_esercizio":saldi_esercizio, "totale_ordinarie_scale":totale_ordinarie_scale, "totale_ordinarie":totale_ordinarie,
                                                                       "totale_ordinarie_comuni":totale_ordinarie_comuni, "totale_utente_manutenzioni_ordinarie":totale_utente_manutenzioni_ordinarie, "totale_generali":totale_generali, "totale_straordinarie": totale_straordinarie})
    
#NOTIFICATION SYSTEM
#view che mette in lista tutte le notifiche

@login_required(login_url="/login")
def notifiche(request):
    notifications = request.user.notifications.all()
    notifications_count = notifications.count()
            
    return render(request, 'Condominio_main/notifiche.html', {"notifications":notifications, "notifications_count": notifications_count})


