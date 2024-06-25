from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'Condominio_main/homepage.html')

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
    else:
        form = RegisterForm
    
    return render(request, 'registration/sign_up.html', {"form" : form})

def my_login(request):
    pass

def dashboard(request):
    pass