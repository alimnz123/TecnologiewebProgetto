from django.test import TestCase, Client
from Condominio.models import Spesa, Fornitore
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
# Create your tests here.

""" # primo test su un model : Spesa e di cui testiamo anche la funzione __str__
class SpesaTestCase(TestCase):
    def setUp(self):
        self.forntore = Fornitore.objects.create(nome="Vetrate")
        self.spesa = Spesa.objects.create(id=15, fornitore="Vetrate", data="2024-03-12", descrizione="Lucidatura vetri", importo=40 )

#test che non si possano creare due spese con lo stesso id
    def test_unique_api_id(self):
        with self.assertRaises(IntegrityError):
            Spesa.objects.create(
                id = 15,
                fornitore = "Vetrate",
                data="2024-03-13", 
                descrizione="Lucidatura vetri - 2",
                importo = 40
            )

# test che di default le spese sia spese diverse
    def test_spese_diverse_by_default(self):
        self.assertEqual(self.spesa, "Spese Diverse")

#testo il metodo str
    def test_str(self):
        expected  = "Spesa Spese Diverse del 2024-03-12 di importo: 40 €"
        actual = str(self.spesa)
        self.assertEqual(expected, actual)

#test homepage
class HomePageTest(TestCase):
    def setUp(self):
        self.client=Client()
    
    def test_home_page_view(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)

#test Profiloview, mi assicuro che l'utente sia loggato
class ProfiloViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='password')

    def test_profile_view(self):
        self.client.login(username='user', password='password')
        response = self.client.get('/profilo')
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get('/profilo')
        self.assertEqual(response.status_code, 302) """


# primo test su un model : Spesa e di cui testiamo anche la funzione __str__
class FornitoreTestCase(TestCase):
    def setUp(self):
        self.forntore = Fornitore.objects.create(nome="Vetrate")

#test che non si possano creare due fornitori con lo stesso pk
    def test_unique_nome(self):
        with self.assertRaises(IntegrityError):
            Fornitore.objects.create(
                nome = "Vetrate"
            )

# test che di default le spese sia spese diverse
    def test_fornitore_indirizzo_by_default(self):
        self.assertEqual(self.forntore.indirizzo, "non dichiarato")

#testo il metodo str
    def test_str(self):
        expected  = "Vetrate"
        actual = str(self.forntore)
        self.assertEqual(expected, actual)

#test login - unica pagina senza bisogno di accesso preventivo
class LoginPageTest(TestCase):
    def setUp(self):
        self.client=Client()
    
    def test_login_page_view(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200) 

#test Profiloview, mi assicuro che l'utente sia loggato
class ProfiloViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='password')

    def test_profile_view(self):
        self.client.login(username='user', password='password')
        response = self.client.get('/profilo')
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get('/profilo')
        self.assertEqual(response.status_code, 302)