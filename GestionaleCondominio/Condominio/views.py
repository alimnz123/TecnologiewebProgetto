from django.shortcuts import render, redirect
from .forms import RegisterForm, InternoForm, LettereConvocazioneForm, VerbaleForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from .models import Verbale, Lettera_Convocazione

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
