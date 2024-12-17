from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.conf import settings

# Create your models here.

# condominio
class Condominio(models.Model):
    nome = models.CharField(verbose_name="Condominio", max_length=100, primary_key=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Condomini"


class Interno(models.Model):
    condomino = models.ForeignKey(User, on_delete=models.PROTECT)
    palazzina = models.ForeignKey(Condominio, on_delete=models.PROTECT, default="Salgari")
    numero_interno = models.CharField(verbose_name="Numero Interno", max_length=50, primary_key=True)
    millesimi_generali = models.FloatField(verbose_name="Millesimi generali")
    millesimi_scala = models.FloatField(verbose_name="Millesimi Scala")
    # millesimi_edificio=models.FloatField(verbose_name="Millesimi Edificio")
    # proprietario=models.TextChoices(verbose_name="Proprietà", choices=User.last_name)
    # da verificare questi elementi
    in_affitto = models.BooleanField(verbose_name="In affitto")
    # occupante=models.TextChoices(verbose_name="Inquilino", choices=User.last_name)
    # mappali = models.CharField(verbose_name="Mappali", max_length=100)

    def __str__(self):
        out=self.numero_interno + " - " + str(self.condomino.last_name)
        return out
    class Meta:
        ordering = ["numero_interno"]
        verbose_name_plural = "Interni"


class Verbale(models.Model):  # lettera di convocazione (ora, giorno, luogo) probabilmente in bacheca + contabilità(rendiconto, consuntivo, dell'anno precedente, appena concluso)
    data = models.DateField("Data", primary_key=True)
    descrizione = models.CharField(max_length=200)
    documento = models.FileField("Documento", upload_to='files/', blank=True, default=None)
    lettera_accompagnatoria = models.FileField(
        "Lettera accompagnatoria", upload_to="files/", blank=True, default=None) 

    def totale_verbali(self):
        totale = self.all().count()
        if totale == 0:
            messaggio = f"Non ci sono verbali disponibili"
        else:
            messaggio = f"Ci sono {totale} verbali disponibili"
        return messaggio

    class Meta:
        ordering = ["data"]
        verbose_name_plural = "Verbali"


class Lettera_Convocazione(models.Model):
    data = models.DateField("Data", primary_key=True)
    descrizione = models.CharField(max_length=200)
    convocazione_documento = models.FileField(
        verbose_name="Lettera di convocazione", upload_to='files/', blank=True, default=None)

    def cancella_dopo_un_mese(self):
        data_verificare = self.data
        if data_verificare - timezone.now < datetime.timedelta(30):
            Lettera_Convocazione.objects.filter(data=data_verificare).delete()
            messaggio = f"Non ci sono lettre di convocazione al momento"
        else:
            messaggio = f"C'è una lettera di convocazione, vai a leggerla!"
        return messaggio

    class Meta:
        verbose_name_plural = "Lettere di convocazione"


class DocumentiPalazzo(models.Model):
    data = models.DateTimeField("Data", primary_key=True)
    descrizione = models.CharField(max_length=200)
    file_documento = models.FileField(verbose_name="Documento del Palazzo", upload_to='files/', blank=True, default=None)

    class Meta:
        verbose_name_plural = "Documenti del Palazzo"


# PARTE RELATIVA ALLE SPESE
class Fornitore(models.Model):
    nome = models.CharField(max_length=100, primary_key=True)
    contratto = models.FileField(verbose_name="Contratto", upload_to='files/', blank=True, default=None)
    indirizzo = models.CharField(max_length=200, blank=True)
    ragione_sociale = models.CharField(max_length=100, blank=True)
    partita_iva = models.CharField(max_length=100, blank=True)
    cf = models.CharField(max_length=100, blank=True)
    iban = models.CharField(max_length=200, blank=True)
    # indirizzo, ragione sociale, partita iva, cf, iban, le fatture vanno pagate attraverso bonifici, f24

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Fornitori"

class Spesa(models.Model):
    class Tipologie(models.TextChoices):
        LUCE_PALAZZINA="Luce Palazzina"
        SCALE_PALAZZINA="Scale Palazzina"
        MANUTENZIONE_ORDINARIA="Manutenzione Ordinaria"
        MANUTENZIONE_ORDINARIA_COMUNE="Manutenzione Ordinaria Comune"
        MANUTENZIONE_ORDINARIA_SCALA="Manutenzione Ordinaria Scala"
        SPESA_GENERALE="Spese Generali"
        SPESA_STRAORDINARIA="Spese Straordinarie"
        SPESA_STRAORDINARIA_EDIFICIO="Spesa Straordinaria Edificio"
        SPESA_STRAORDINARIA_SCALE="Spesa Straordinaria Scale"
        SPESA_STRAORDINARIA_ANTENNE="Spesa Straordinaria Antenne"
        SPESE_DIVERSE="Spese Diverse"
        
    fornitore=models.ForeignKey(Fornitore, on_delete=models.PROTECT, default=None)
    data=models.DateField("Data")
    #documento=models.FileField("File", blank=True, default=None)
    tipologia=models.TextField("Tipologia", choices=Tipologie.choices, default=Tipologie.SPESE_DIVERSE, max_length=200)
    descrizione=models.CharField(default=None, max_length=200)
    assegnatario=models.ManyToManyField(Interno) 
    importo=models.FloatField("Totale", default=0)
    class Meta:
        verbose_name_plural="Spese"
