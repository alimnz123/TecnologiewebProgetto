from django import template
from django.db.models import Q

register = template.Library()

from Condominio.models import * 
  
@register.filter(name="get_interno")
def get_interno(value):
    return value.numero_interno

@register.filter(name="get_cognome")
def get_cognome(value):
    condomino=value.condomino
    return condomino.last_name

@register.filter(name="get_millesimi_generali")
def get_millesimi_generali(value):
    return value.millesimi_generali

@register.filter(name="get_millesimi_scala")
def get_millesimi_scala(value):
    return value.millesimi_scala


@register.filter(name="get_spese_straordinarie_edifici")
def get_spese_straordinarie_edifici(value):
    
    spese_straordinarie_edifici=Spesa.objects.filter(Q(tipologia="Spesa Straordinaria Edificio") & Q(data__year=current_year))

    totale_spese_straordinarie_edifici = 0
    for spesa in spese_straordinarie_edifici:
        totale_spese_straordinarie_edifici += spesa.importo

    return value.millesimi_scala
    