from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegisterForm, InternoForm, LettereConvocazioneForm, VerbaleForm, DocumentiPalazzoForm, FornitoreForm, SpesaForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.views.generic.edit import UpdateView
from .models import Verbale, Lettera_Convocazione, DocumentiPalazzo, Fornitore, Spesa

# Create your views here.

@login_required(login_url="/login")
def homepage(request):
    return render(request, 'Condominio_main/homepage.html')

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

@login_required(login_url="/login")
def documenti_palazzo(request):
    documenti=DocumentiPalazzo.objects.all()

    if request.method == "POST":
        documento_id = request.POST.get("documento-id")
        print(documento_id)
        documento=DocumentiPalazzo.objects.filter(id=documento_id).first()
        if documento and (documento.author == request.user or request.user.has_perm("main.delete_documento")):
            documento.delete()

    return render(request, 'Condominio_main/documenti_palazzo.html', {"documento":documenti})


@login_required(login_url="/login")
def create_interno(request):
    if request.method == 'POST':
        form = InternoForm(request.POST)
        if form.is_valid():
            interno = form.save(commit=False)
            interno.author = request.user
            interno.save()
            return redirect("/home")
    else:
        form = InternoForm()

    return render(request, 'Condominio_main/create_interno.html', {"form": form})

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
            return redirect("/home")
    else:
        form = DocumentiPalazzoForm()

    return render(request, 'Condominio_main/create_documento.html', {"form": form})


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


def dashboard(request):
    pass


#views related to Fornitori and Spese
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

@login_required(login_url="/login")
def spesa(request):
    spese=Spesa.objects.all()

    if request.method == "POST":
        spesa_id = request.POST.get("spesa-id")
        print(spesa_id)
        spesa=Spesa.objects.filter(id=spesa_id).first()
        if spesa and (spesa.author == request.user or request.user.has_perm("main.delete_spesa")):
            spesa.delete()
            
    return render(request, 'Condominio_main/spese.html', {"spese":spese})

class UpdateSpesaView(UpdateView):
    model = Spesa
    template_name = "Condominio_main/edit_spesa.html"
    fields = "__all__"
    
    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("spesa")