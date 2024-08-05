from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="home"),
    
    path('home', views.homepage, name="home"),

    path('sign-up', views.sign_up, name="sign_up"),

    path('my-login', views.my_login, name="Login"),

    path('create_interno', views.create_interno, name="create_interno"),

    path('create_lettera', views.create_lettera, name="create_lettera"),

    path('create_verbale', views.create_verbale, name="create_verbale"),
        
]
