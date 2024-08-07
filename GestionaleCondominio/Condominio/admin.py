from django.contrib import admin
from .models import DocumentiPalazzo, Verbale, Lettera_Convocazione

# Register your models here.
admin.site.register(DocumentiPalazzo)
admin.site.register(Verbale)
admin.site.register(Lettera_Convocazione)
