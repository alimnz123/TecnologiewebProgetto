from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="home"),
    
    path('home', views.homepage, name="home"),


    path('sign-up', views.sign_up, name="sign_up"),

    path('my-login', views.my_login, name="Login"),

    path('dashboard', views.dashboard, name="Dashboard"),

        
]
