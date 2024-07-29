from django.db import models
from django.contrib.auth.models import User 
import datetime
from django.utils import timezone

# Create your models here.

#condominio
class Condominio(models.Model):
    nome=models.CharField(verbose_name="Condominio", max_length=100, primary_key=True)
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name_plural="Condomini"

class Interno(models.Model):
    condomino = models.ForeignKey(User, on_delete=models.CASCADE)
    palazzina=models.ForeignKey(Condominio, on_delete=models.CASCADE)
    numero=models.CharField(verbose_name="Numero", max_length=50, primary_key=True)
    millesimi_generali=models.FloatField(verbose_name="Millesimi generali")
    millesimi_scala=models.FloatField(verbose_name="Millesimi Scala")
    #proprietario=models.TextChoices(verbose_name="Proprietà", choices=User.last_name)
    #da verificare questi elementi
    in_affitto=models.BooleanField(verbose_name="In affitto")    
    #occupante=models.TextChoices(verbose_name="Inquilino", choices=User.last_name)
    mappali=models.CharField(verbose_name="Mappali", max_length=100)

""" class Palazzina(models.Model):
    condominio=models.ForeignKey(Condominio, verbose_name="Condominio", on_delete=models.CASCADE)
    numero=models.CharField(verbose_name="Numero", max_length=50, primary_key=True)

    def __str__(self):
        return f"La palazzina {self.numero} del condominio {self.condominio}"
    class Meta:
        verbose_name_plural="Palazzine" """

""" class Interno(models.Model):
    condominio=models.ForeignKey(Condominio, on_delete=models.CASCADE)
    #palazzina=models.ForeignKey(Palazzina, verbose_name="Palazzina", on_delete=models.CASCADE)
    numero=models.CharField(verbose_name="Numero", max_length=50, primary_key=True)
    millesimi_generali=models.FloatField(verbose_name="Millesimi generali")
    millesimi_scala=models.FloatField(verbose_name="Millesimi Scala")
    proprietario=models.TextChoices(verbose_name="Proprietà", choices=Condomino.cognome)
    in_affitto=models.BooleanField(verbose_name="In affitto")    
    occupante=models.TextChoices(verbose_name="Inquilino", choices=Condomino.cognome)
    mappali=models.CharField(verbose_name="Mappali", max_length=100)
    

    def __str__(self):
        return f"L'interno numero {self.numero} ha {self.millesimi_generali} e {self.millesimi_scala} e i valori mappali sono {self.mappali}."
    class Meta:
        verbose_name_plural="Interni"


class Verbale(models.Model): #lettera di convocazione (ora, giorno, luogo) probabilmente in bacheca + contabilità(rendiconto, consuntivo, dell'anno precedente, appena concluso)
    data=models.DateTimeField("Data", primary_key=True)
    descrizione=models.CharField(max_length=200)
    documento=models.FileField("Documento", blank=True, default=None)
    lettera_accompagnatoria=models.FileField("Lettera accompagnatoria", blank=True, default=None)

    def totale_verbali(self):
        totale = self.all().count()
        if totale == 0:
            messaggio = f"Non ci sono verbali disponibili"
        else:
            messaggio = f"Ci sono {totale} verbali disponibili"
        return messaggio
    class Meta:
        ordering = ["data"]
        verbose_name_plural="Verbali"

class Lettera_Convocazione(models.Model):
    data=models.DateTimeField("Data", primary_key=True)
    descrizione=models.CharField(max_length=200)
    convocazione_documento=models.FileField(verbose_name="Lettera di convocazione", blank=True, default=None)
    def cancella_dopo_un_mese(self):
        data_verificare=self.data
        if data_verificare - timezone.now < datetime.timedelta(30):
            Lettera_Convocazione.objects.filter(data=data_verificare).delete()
            messaggio=f"Non ci sono lettre di convocazione al momento"
        else:
            messaggio=f"C'è una lettera di convocazione, vai a leggerla!"
        return messaggio
    class Meta:
        verbose_name_plural="Lettere di convocazione" """