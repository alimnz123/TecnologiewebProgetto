from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# Create your views here.

@login_required(login_url="/login")
def homepage(request):
    return render(request, 'Condominio_main/homepage.html')

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # i want to create a new user
        if form.is_valid():
            user= form.save()
            login(request, user)
            return redirect('/home')

    else:
        form = RegisterForm()
    
    return render(request, 'registration/sign_up.html', {"form" : form})

def my_login(request):
    pass

def dashboard(request):
    pass