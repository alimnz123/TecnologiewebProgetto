from django import template
from django.db.models import Q
import datetime

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
    current_date = datetime.datetime.now()
    current_year = current_date.year

    spese_straordinarie_edificio=Spesa.objects.filter(Q(tipologia="Spesa Straordinaria Edificio") & Q(data__year=current_year) & Q(assegnatario=value))

    totale_spese_straordinarie_edificio = 0
    for spesa in spese_straordinarie_edificio:
        totale_spese_straordinarie_edifici += spesa.importo

    return (totale_spese_straordinarie_edificio / 1000) * value.millesimi_generali
    
@register.filter(name="get_spese_straordinarie_scala")
def get_spese_straordinarie_scala(value):
    current_date = datetime.datetime.now()
    current_year = current_date.year

    spese_straordinarie_scala = Spesa.objects.filter(Q(tipologia="Spesa Straordinaria Scale") & Q(data__year=current_year) & Q(assegnatario=value))

    totale_spese_straordinarie_scala = 0
    for spesa in spese_straordinarie_scala:
        totale_spese_straordinarie_scala += spesa.importo

    return (totale_spese_straordinarie_scala / 1000) * value.millesimi_scala
    
@register.filter(name="get_spese_straordinarie_antenne")
def get_spese_straordinarie_antenne(value):
    current_date = datetime.datetime.now()
    current_year = current_date.year

    spese_straordinarie_antenne=Spesa.objects.filter(Q(tipologia="Spesa Straordinaria Antenne") & Q(data__year=current_year) & Q(assegnatario=value))

    totale_spese_straordinarie_antenne = 0
    for spesa in spese_straordinarie_antenne:
        totale_spese_straordinarie_antenne += spesa.importo

    return (totale_spese_straordinarie_antenne / 1000) * value.millesimi_generali

@register.filter(name="get_spese_diverse")
def get_spese_diverse(value):
    current_date = datetime.datetime.now()
    current_year = current_date.year

    spese_diverse=Spesa.objects.filter(Q(tipologia="Spese Diverse") & Q(data__year=current_year) & Q(assegnatario=value))

    totale_spese_diverse = 0
    for spesa in spese_diverse:
        totale_spese_diverse += spesa.importo

    return (totale_spese_diverse / 1000) * value.millesimi_generali

@register.filter(name="get_manutenzione_ordinaria_scala")
def get_manutenzione_ordinaria_scala(value):
    current_date = datetime.datetime.now()
    current_year = current_date.year

    spese_ordinarie_scale=Spesa.objects.filter(Q(tipologia="Manutenzione Ordinaria Scala") & Q(data__year=current_year) & Q(assegnatario=value))

    totale_ordinarie_scale = 0
    for spesa in spese_ordinarie_scale:
        totale_ordinarie_scale += spesa.importo 

    return (totale_ordinarie_scale / 1000) * value.millesimi_scala

@register.filter(name="get_manutenzione_ordinaria")
def get_manutenzione_ordinaria(value):
    current_date = datetime.datetime.now()
    current_year = current_date.year

    spese_ordinarie=Spesa.objects.filter(Q(tipologia="Manutenzione Ordinaria") & Q(data__year=current_year) & Q(assegnatario=value))

    totale_ordinarie = 0
    for spesa in spese_ordinarie:
        totale_ordinarie += spesa.importo

    return (totale_ordinarie / 1000) * value.millesimi_generali

@register.filter(name="get_manutenzione_ordinaria_aree_comuni")
def get_manutenzione_ordinaria_aree_comuni(value):
    current_date = datetime.datetime.now()
    current_year = current_date.year

    spese_ordinarie_comuni=Spesa.objects.filter(Q(tipologia="Manutenzione Ordinaria Comune") & Q(data__year=current_year) & Q(assegnatario=value))

    totale_ordinarie_comuni = 0
    for spesa in spese_ordinarie_comuni:
        totale_ordinarie_comuni += spesa.importo

    return (totale_ordinarie_comuni / 1000) * value.millesimi_generali

@register.filter(name="get_generali")
def get_generali(value):
    current_date = datetime.datetime.now()
    current_year = current_date.year

    spese_generali=Spesa.objects.filter(Q(tipologia="Spese Generali") & Q(data__year=current_year) & Q(assegnatario=value))

    totale_generali = 0
    for spesa in spese_generali:
        totale_generali += spesa.importo

    return (totale_generali / 1000) * value.millesimi_generali

@register.filter(name="get_straordinarie")
def get_straordinarie(value):
    current_date = datetime.datetime.now()
    current_year = current_date.year

    spese_straordinarie=Spesa.objects.filter(Q(tipologia="Spese Straordinarie") & Q(data__year=current_year) & Q(assegnatario=value))

    totale_straordinarie = 0
    for spesa in spese_straordinarie:
        totale_straordinarie += spesa.importo

    return (totale_straordinarie / 1000) * value.millesimi_generali

@register.filter(name="get_totale_esercizio")
def get_totale_esercizio(value):

    return "%.2f" % (get_spese_straordinarie_scala(value) + get_spese_straordinarie_antenne(value) + get_spese_diverse(value) + get_manutenzione_ordinaria_scala(value) + get_manutenzione_ordinaria(value) + get_manutenzione_ordinaria_aree_comuni(value) + get_generali(value) + get_straordinarie(value))


@register.filter(name="generali_previsionali")
def generali_previsionali(value):

    return get_generali(value) + (get_generali(value) * (0.1))

@register.filter(name="straordinarie_edifici_previsionali")
def straordinarie_edifici_previsionali(value):

    return get_spese_straordinarie_edifici(value) + (get_spese_straordinarie_edifici(value) * (0.1))

@register.filter(name="straordinarie_previsionali")
def straordinarie_previsionali(value):

    return get_straordinarie(value) + (get_straordinarie(value) * (0.1))

@register.filter(name="ordinarie_scala_previsionali")
def ordinarie_scala_previsionali(value):

    return get_manutenzione_ordinaria_scala(value) + (get_manutenzione_ordinaria_scala(value) * (0.1))

@register.filter(name="ordinarie_previsionali")
def ordinarie_previsionali(value):

    return get_manutenzione_ordinaria(value) + (get_manutenzione_ordinaria(value) * (0.1))

@register.filter(name="totale_previsionali")
def totale_previsionali(value):

    return ordinarie_previsionali(value) + ordinarie_scala_previsionali(value) + generali_previsionali(value) + straordinarie_edifici_previsionali(value) + straordinarie_edifici_previsionali(value) + straordinarie_previsionali(value) 
