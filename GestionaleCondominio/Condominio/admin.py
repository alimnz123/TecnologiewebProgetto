from django.contrib import admin
from .models import DocumentiPalazzo, Verbale, Lettera_Convocazione, Spesa, Fornitore

# Register your models here.
admin.site.register(DocumentiPalazzo)
admin.site.register(Verbale)
admin.site.register(Lettera_Convocazione)
admin.site.register(Spesa)
admin.site.register(Fornitore)


