from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name="home"),
    
    path('home', views.homepage, name="home"),

    path('sign-up', views.sign_up, name="sign_up"),

    path('login', views.my_login, name="login"),

    path('logout', views.logout_view, name="logout"),

    path('profilo', views.profilo_utente, name="profilo"),

    path('success', views.success, name="success"),

    path('interni', views.interno, name="interni"),

    path("edit_interno/<pk>/", views.UpdateInternoView.as_view(), name="edit_interno"),

    path('create_interno/', views.create_interno, name="create_interno"),

    path("cancella_interno/<pk>/", views.DeleteInternoView.as_view(),name="cancella_interno"),
    
    path('create_lettera', views.create_lettera, name="create_lettera"),

    path("cancella_lettera/<pk>/", views.DeleteLetteraConvocazioneView.as_view(),name="cancella_lettera"),

    path('create_verbale/', views.create_verbale, name="create_verbale"),

    path("cancella_verbale/<pk>/", views.DeleteVerbaleView.as_view(),name="cancella_verbale"),

    path('create_documento/', views.create_documento, name="create_documento"),

    path("cancella_documento/<pk>/", views.DeleteDocumentiPalazzoView.as_view(),name="cancella_documento_palazzo"),

    path('bacheca/', views.bacheca, name="bacheca"),

    path('documenti_palazzo', views.documenti_palazzo, name="documenti_palazzo"),

    path('fornitori', views.fornitori, name="fornitori"),

    path('create_fornitore', views.create_fornitore, name="create_fornitore"),

    path("edit_fornitore/<pk>/", views.UpdateFornitoreView.as_view(), name="edit_fornitore"),

    path("cancella_fornitore/<pk>/", views.DeleteFornitoreView.as_view(),name="cancella_fornitore"),

    path('spesa/', views.spesa, name="spesa"),

    path('create_spesa/', views.create_spesa, name="create_spesa"),

    path("<pk>/edit_spesa/", views.UpdateSpesaView.as_view(), name="edit_spesa"),

    path("cancella_spesa/<pk>/", views.DeleteSpesaView.as_view(),name="cancella_spesa"),

    path("riparto_preventivo/", views.RipartoPreventivo, name="riparto_preventivo"),

    path("riparto_consuntivo/", views.RipartoConsuntivo, name="riparto_consuntivo"),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
