from django.contrib import admin
from .models import DocumentiPalazzo, Verbale, Lettera_Convocazione, Spesa, Fornitore, Interno, Condominio, Notifica

# Register your models here.
admin.site.register(Notifica)
admin.site.register(Condominio)
admin.site.register(Interno)
admin.site.register(DocumentiPalazzo)
admin.site.register(Verbale)
admin.site.register(Lettera_Convocazione)
admin.site.register(Spesa)
admin.site.register(Fornitore)


