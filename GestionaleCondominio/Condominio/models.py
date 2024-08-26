from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# Create your models here.

# condominio
class Condominio(models.Model):
    nome = models.CharField(verbose_name="Condominio", max_length=100, primary_key=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Condomini"


class Interno(models.Model):
    condomino = models.ForeignKey(User, on_delete=models.CASCADE)
    palazzina = models.ForeignKey(Condominio, on_delete=models.CASCADE, default="Salgari")
    numero_interno = models.CharField(verbose_name="Numero Interno", max_length=50, primary_key=True)
    millesimi_generali = models.FloatField(verbose_name="Millesimi generali")
    millesimi_scala = models.FloatField(verbose_name="Millesimi Scala")
    millesimi_edificio=models.FloatField(verbose_name="Millesimi Edificio")
    # proprietario=models.TextChoices(verbose_name="Proprietà", choices=User.last_name)
    # da verificare questi elementi
    in_affitto = models.BooleanField(verbose_name="In affitto")
    # occupante=models.TextChoices(verbose_name="Inquilino", choices=User.last_name)
    mappali = models.CharField(verbose_name="Mappali", max_length=100)
    class Meta:
        ordering = ["numero_interno"]
        verbose_name_plural = "Interni"


class Verbale(models.Model):  # lettera di convocazione (ora, giorno, luogo) probabilmente in bacheca + contabilità(rendiconto, consuntivo, dell'anno precedente, appena concluso)
    data = models.DateTimeField("Data", primary_key=True)
    descrizione = models.CharField(max_length=200)
    documento = models.FileField("Documento", blank=True, default=None)
    lettera_accompagnatoria = models.FileField(
        "Lettera accompagnatoria", blank=True, default=None)

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
    data = models.DateTimeField("Data", primary_key=True)
    descrizione = models.CharField(max_length=200)
    convocazione_documento = models.FileField(
        verbose_name="Lettera di convocazione", blank=True, default=None)

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
    file_documento = models.FileField(verbose_name="Documento del Palazzo", blank=True, default=None)

    class Meta:
        verbose_name_plural = "Documenti del Palazzo"


# PARTE RELATIVA ALLE SPESE
class Fornitore(models.Model):
    nome = models.CharField(max_length=100, primary_key=True)
    contratto = models.FileField("Contratto", blank=True, default=None)
    indirizzo = models.CharField(max_length=200)
    ragione_sociale = models.CharField(max_length=100)
    partita_iva = models.CharField(max_length=100)
    cf = models.CharField(max_length=100)
    iban = models.CharField(max_length=200)
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
        SPESA_GENERALE="Spese Generali"
        SPESA_STRAORDINARIA="Spesa Straordinaria"
        SPESA_STRAORDINARIA_COMUNE="Spesa Straordinaria Comune"
        SPESE_DIVERSE="Spese Diverse"
        
    fornitore=models.ForeignKey(Fornitore, on_delete=models.PROTECT, default=None)
    data=models.DateTimeField("Data")
    #documento=models.FileField("File", blank=True, default=None)
    tipologia=models.TextField("Tipologia", choices=Tipologie.choices, default=Tipologie.SPESE_DIVERSE, max_length=200)
    descrizione=models.CharField(default=None, max_length=200)
    assegnatario=models.ManyToManyField(User) 
    importo=models.FloatField("Totale", default=0)
    class Meta:
        verbose_name_plural="Spese"

#NOTIFICATION SYSTEM
class Notification(models.Model):
    message = models.TextField("Hai un nuovo messaggio in bacheca")
    users = models.ManyToManyField(User, through='UserNotification')

class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_seen = models.BooleanField()





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
        verbose_name_plural="Lettere di convocazione" 
        
        
class Fornitore(models.Model): 
    nome=models.CharField(max_length=100, primary_key=True)
    contratto=models.FileField("Contratto", blank=True, default=None)
    indirizzo=models.CharField(max_length=200)
    ragione_sociale=models.CharField(max_length=100)
    partita_iva=models.CharField(max_length=100)
    cf=models.CharField(max_length=100)
    iban=models.CharField(max_length=200)
    #indirizzo, ragione sociale, partita iva, cf, iban, le fatture vanno pagate attraverso bonifici, f24
    def __str__(self) :
        return self.nome
    class Meta:
        verbose_name_plural="Fornitori"

#da qui in poi cambia tutto
class Spese_Fornitore(models.Model):
    # class Palazzina(models.TextChoices):
    #     A="A"
    #     B="B"
    #     C="C"
    class Tipologie(models.TextChoices):
        ORDINARIE="Ordinaria Manutenzione"
        STRAORDINARIE="Straordinaria Manutenzione"
        ALTRO="Altro"
    class Ordinarie(models.TextChoices): #importo totale diviso 1000 * millesimi generali, mentre *millesimi scale se l'importo è legato a luce scala o pulizia scale
        VERDE="Manutenzione aree verdi"
        LUCE="Luce condominiale"
        ACQUA="Acqua condominiale" #unica giardino o divisa se contatore unico per tutto il palazzo, se giardino comune il costo al m3 viene moltiplicato allo stesso modo per i millesimi generali
        GAS="Gas condominiale"
        FOGNATURE="Fognature" #mill gen
        PULIZIASCALE="Pulizia Scale" #mill scale
        ALTRO="Altro"
    fornitore=models.ForeignKey(Fornitore, on_delete=models.PROTECT)
    data=models.DateTimeField("Data")
    documento=models.FileField("File", blank=True, default=None)
    tipologia=models.TextField("Tipologia", choices=Tipologie.choices, default=Tipologie.ALTRO, max_length=200)
    if tipologia == "Ordinaria manutenzione":
        ordinarie=models.TextField("Ordinarie", choices=Ordinarie.choices, default=Ordinarie.ACQUA)
    descrizione=models.CharField(default=None, max_length=200)
    #palazzina=models.Choices("Palazzina", choices=Palazzina.numero)
    importo_totale=models.FloatField("Totale", default=0)
    #per ogni tipologia di spesa definisci il totale per anno

    class Meta:
        verbose_name_plural="Spese Clienti"

#riparto consuntivo 2022 di fine anno
class Riparto_Consuntivo(models.Model):
    data=models.DateTimeField(primary_key=True)
    #palazzina=models.CharField(verbose_name="palazzina", max_length=100, default=None)
    interno=models.OneToOneField(Interno, verbose_name="Interno", max_length=100, on_delete=models.CASCADE)
    #nome, cognome, in_affitto, millesimi generali e scala, vanno messi o li deduco ????
    #nome = models.CharField(verbose_name="Nome", max_length=100)
    #cognome=models.CharField(verbose_name="Cognome", max_length=100)
    #in_affitto=models.BooleanField(verbose_name="In Affitto")
    #if in_affitto is True:
    #    proprietà=models.CharField(verbose_name="Proprietà")
    millesimi_generali=models.FloatField(verbose_name="Millesimi generali")
    millesimi_scala=models.FloatField(verbose_name="Millesimi scala")
    spese_straordinarie_edificio=models.FloatField(verbose_name="Spese straordinarie edificio",  default=0)
    spese_straordinarie_scala=models.FloatField(verbose_name="Spese straordinarie scala",  default=0)
    spese_straordinarie_antenna=models.FloatField(verbose_name="Spese straordinarie antenna",  default=0)
    spese_diverse=models.FloatField(verbose_name="Spese diverse",  default=0)
    manutenzione_ordinaria_scala=models.FloatField(verbose_name="Manutenzione ordinaria scala",  default=0)
    manutenzione_ordinaria=models.FloatField(verbose_name="Manutenzione ordinaria",  default=0)
    manutenzione_ordinaria_comuni=models.FloatField(verbose_name="Manuteznione ordinaria comuni",  default=0)
    totale_inquilino=models.FloatField(verbose_name="Totale inquilino",  default=0)
    spese_generali=models.FloatField(verbose_name="Spese generali",  default=0)
    spese_straordianrie=models.FloatField(verbose_name="Spese straordinarie",  default=0)
    totale_esercizio=models.FloatField(verbose_name="Totale esercizio",  default=0) #totale effettivo speso
    saldo_esercizio_precedente=models.FloatField(verbose_name="Saldo esercizio precedente", default=0) #Condomino.saldo_esercizio_precedente #quanto avanza dall'esercizio precedente
    totale_complessivo=models.FloatField(verbose_name="Totale complessivo",  default=0) #totale esercizio-saldo esercizio precedente
    versamenti_anno_precedente=models.FloatField(verbose_name="Versamenti anno precedente", default=0) #quanto ho versato nel 2022 secondo le rate dovute da preventivo 2023
    saldi_di_esercizio=models.FloatField(verbose_name="Saldi di esercizio",  default=0) #totale complessivo - versamenti 2022
    
    #definisci le spese straordinarie edificio per utente
    def _spese_straordinarie_edificio_(self):
        pass
    #definisci spese str scala
    def _calcolo_straordinarie_scala_(self):
        pass
    #definisci spese str antenna
    def _calcolo_straordinarie_antenna_(self):
        pass
    #definisci spese diverse
    def _calcolo_spese_diverse_(self):
        pass
    #definisci manutenzione ordinarie scale
    def _calcolo_manutenzione_ordinarie_scala_(self):
        pass
    #definisci manutenzione ordinaria
    def _calcolo_manutenzione_ordinaria_(self):
        pass
    #definisci manutenzione ordinaria comuni
    def _calcolo_manutenzione_ordinaria_comuni_(self):
        pass
    #totale inquilino
    def _calcola_totale_inquilino_(self):
        pass
    #spese generali
    #spese straordinarie
    #totale esercizio
    #saldo esercizio precedente
    #totale complessivo
    #versamenti anno precedente
    #saldi di esercizio
    class Meta:
        verbose_name_plural="Riparti consuntivi"

#riparto preventivo  inizio 2023
class Riparto_Preventivo(models.Model):
    data=models.DateTimeField(primary_key=True)
    #palazzina=models.CharField(verbose_name="palazzina", max_length=100, default=None)
    interno=models.OneToOneField(Interno, verbose_name="Interno", max_length=100, on_delete=models.CASCADE)
    #nome=models.CharField(verbose_name="Nome", max_length=100)
    #cognome=models.CharField(verbose_name="Cognome", max_length=100)
    #in_affitto=models.BooleanField(verbose_name="In Affitto")
    #if in_affitto is True:
    #proprietà=models.CharField(verbose_name="Proprietà", max_length=100, default=None)
    spese_generali=models.FloatField(verbose_name="Spese generali",  default=0) #presunti e rialzati di una percentuale
    spese_straordinarie_palazzine=models.FloatField(verbose_name="Spese straordinarie palazzine",  default=0) #presunti e rialzati di una percentuale
    spese_straordianrie=models.FloatField(verbose_name="Spese straordinarie", default=0) #presunti e rialzati di una percentuale
    totale_esercizio=models.FloatField(verbose_name="Totale esercizio",  default=0) #spese generali + straordinarie palazzina e straordinarie
    saldo_esercizio_precedente = models.FloatField(verbose_name="Saldo esercizio precedente",  default=0) #Condomino.saldo_esercizio_precedente
    totale_complessivo = models.FloatField(verbose_name="Totale complessivo",  default=0) #totale esercizio-saldo esercizio precedente
    numero_rate = models.IntegerField(verbose_name="Rate",  default=3)
    valore_rata=models.FloatField(verbose_name="Importo",  default=0)

    def in_affitto(self):
        if self.in_affitto == True :
            proprietà = Interno.inquilino
        else:
            pass
        return proprietà
    #per ogni rate definisci le rate e come vengono ripartite
    def calcolo_rate(self):
        for i in self.rate:
            rata=(self.totale_complessivo%i)
            if self.saldo_esercizio_precedente < 0 :
                da_rendere=self.saldo_esercizio_precedente
                rata= rata + da_rendere
        return rata

    class Meta:
        verbose_name_plural="Riparti preventivo"

 """
