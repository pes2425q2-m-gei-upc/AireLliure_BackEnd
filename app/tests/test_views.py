from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from app.models import *
from django.test import override_settings

@override_settings(ROOT_URLCONF='AireLliure.urls')
class TestViewsUsuari(TestCase):
    
    def setUp(self):
        Usuari.objects.create(
            correu = "test@example.com",
            password = "1234",
            nom = "test",
            estat = "inactiu",
            punts = 0,
            deshabilitador = None,
            about = "hola mundo",
            administrador = False
        )
        Usuari.objects.create(
            correu = "test2@example.com",
            password = "1234",
            nom = "test2",
            estat = "inactiu",
            punts = 0,
            deshabilitador = None,
            about = "hola mundo 2",
            administrador = False
        )
    
    def test_get_usuaris_all(self):
        url = reverse("get_usuaris")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["correu"], "test@example.com")
        self.assertEqual(response.data[1]["correu"], "test2@example.com")
        
    def test_get_usuari_concret(self):
        url = reverse("get_usuari", args=["test@example.com"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["correu"], "test@example.com")
        
    def test_create_usuari(self):
        url = reverse("create_usuari")
        response = self.client.post(url, {
            "correu": "test3@example.com",
            "password": "1234",
            "nom": "test3",
            "estat": "inactiu",
            "punts": 0,
            "deshabilitador": "",
            "about": "hola mundo 3",
            "administrador": False
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Usuari.objects.count(), 3)
        self.assertEqual(Usuari.objects.get(correu="test3@example.com").nom, "test3")

    def test_login_usuari(self):
        url = reverse("login_usuari")
        response = self.client.post(url, {
            "correu": "test@example.com",
            "password": "1234"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
    def test_error_login_usuari(self):
        url = reverse('login_usuari')
        response = self.client.post(url, {
            "correu": "test@example.com",
            "password": "12345"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        
    def test_update_usuari(self):
        url = reverse('update_usuari', args=["test@example.com"])
        response = self.client.patch(url, {
            "nom": "test_updated"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Usuari.objects.get(correu="test@example.com").nom, "test_updated")
        
    def test_eliminar_usuari(self):
        url = reverse('delete_usuari', args=["test@example.com"])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Usuari.objects.count(), 1)
        
    
        
        
        
