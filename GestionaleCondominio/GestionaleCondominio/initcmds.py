from Condominio.models import *

def erase_db():
    print("Cancello il DB")
    Interno.objects.all().delete()
    DocumentiPalazzo.objects.all().delete()
    Fornitore.objects.all().delete()

def init_db():
    
    if len(Interno.objects.all()) != 0:
        return

    internodict = {
        "condomino" : ["Alessandro Manzoni", "George Orwell", "Omero", "George Orwell", "Omero"],
        "titoli" : ["Promessi Sposi", "1984", "Odissea", "La Fattoria degli Animali", "Iliade"],
        "pagine" : [832,328,414,141,263],
    }

    for i in range(5):
        l = Libro()
        for k in libridict:
            if k == "autori":
                    l.autore = libridict[k][i]
            if k == "titoli":
                    l.titolo = libridict[k][i]
            if k == "pagine":
                    l.pagine = libridict[k][i] 
        l.save()
        for _ in range(2):
            c = Copia()
            c.libro = l
            c.save()
    
    print("DUMP DB")
    print(Interno.objects.all()) #controlliamo
    print(DocumentiPalazzo.objects.all())
    print(Fornitore.objects.all())

