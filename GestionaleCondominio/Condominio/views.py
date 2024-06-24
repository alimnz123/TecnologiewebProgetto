from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'main/home.html')

def register(request):
    pass

def my_login(request):
    pass

def dashboard(request):
    pass