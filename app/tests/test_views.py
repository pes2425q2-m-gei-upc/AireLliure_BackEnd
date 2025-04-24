# pylint disable=non-ascii-name, unused-import, wildcard-import, too-many-lines

import json

from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status

from app.forms import AssignaAccesibilitatRespiratoriaForm
from app.models import *  # noqa: F403, F405


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestViewsUsuari(TestCase):

    def setUp(self):
        Usuari.objects.create(
            correu="test@example.com",
            password="1234",
            nom="test",
            estat="inactiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo",
            administrador=False,
        )
        Usuari.objects.create(
            correu="test2@example.com",
            password="1234",
            nom="test2",
            estat="inactiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo 2",
            administrador=False,
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
        response = self.client.post(
            url,
            {
                "correu": "test3@example.com",
                "password": "1234",
                "nom": "test3",
                "estat": "inactiu",
                "punts": 0,
                "deshabilitador": "",
                "about": "hola mundo 3",
                "administrador": False,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Usuari.objects.count(), 3)
        self.assertEqual(Usuari.objects.get(correu="test3@example.com").nom, "test3")

    def test_login_usuari(self):
        url = reverse("login_usuari")
        response = self.client.post(
            url,
            {"correu": "test@example.com", "password": "1234"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_error_login_usuari(self):
        url = reverse("login_usuari")
        response = self.client.post(
            url,
            {"correu": "test@example.com", "password": "12345"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_update_usuari(self):
        url = reverse("update_usuari", args=["test@example.com"])
        response = self.client.patch(
            url, {"nom": "test_updated"}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Usuari.objects.get(correu="test@example.com").nom, "test_updated"
        )

    def test_eliminar_usuari(self):
        url = reverse("delete_usuari", args=["test@example.com"])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Usuari.objects.count(), 1)


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestViewsAdmin(TestCase):
    def setUp(self):
        Admin.objects.create(
            correu="admin@example.com",
            password="1234",
            nom="admin",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo",
            administrador=True,
        )
        Admin.objects.create(
            correu="admin2@example.com",
            password="1234",
            nom="admin2",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo 2",
            administrador=True,
        )

    def test_get_all_admins(self):
        url = reverse("get_admins")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["correu"], "admin@example.com")
        self.assertEqual(response.data[1]["correu"], "admin2@example.com")

    def test_get_admin_concret(self):
        url = reverse("get_admin", args=["admin@example.com"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["correu"], "admin@example.com")

    def test_get_admin_error(self):
        url = reverse("get_admin", args=["admin_error@example.com"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_admin(self):
        url = reverse("create_admin")
        response = self.client.post(
            url,
            {
                "correu": "admin3@example.com",
                "password": "1234",
                "nom": "admin3",
                "estat": "actiu",
                "punts": 0,
                "deshabilitador": "",
                "about": "hola mundo 3",
                "administrador": True,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Admin.objects.count(), 3)
        self.assertEqual(Admin.objects.get(correu="admin3@example.com").nom, "admin3")

    def test_update_admin(self):
        url = reverse("update_admin", args=["admin@example.com"])
        response = self.client.patch(
            url, {"nom": "admin_updated"}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Admin.objects.get(correu="admin@example.com").nom, "admin_updated"
        )

    def test_eliminar_admin(self):
        url = reverse("delete_admin", args=["admin@example.com"])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Admin.objects.count(), 1)


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestViewAmistats(TestCase):
    def setUp(self):
        self.user1 = Usuari.objects.create(
            correu="user1@example.com",
            password="1234",
            nom="user1",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo",
            administrador=False,
        )
        self.user2 = Usuari.objects.create(
            correu="user2@example.com",
            password="1234",
            nom="user2",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo 2",
            administrador=False,
        )
        self.user3 = Usuari.objects.create(
            correu="user3@example.com",
            password="1234",
            nom="user3",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo 3",
            administrador=False,
        )
        # Crear una amistad inicial para las pruebas de actualización y eliminación
        self.amistat = Amistat.objects.create(solicita=self.user1, accepta=self.user2)

    def test_create_amistat(self):
        url = reverse("create_amistat")
        response = self.client.post(
            url,
            {
                "solicita": self.user3.pk,
                "accepta": self.user1.pk,
                "pendent": True,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Amistat.objects.count(), 2)  # Ya existe una amistad en setUp
        self.assertEqual(
            Amistat.objects.get(solicita=self.user3, accepta=self.user1).pk, 2
        )

    def test_get_amistats(self):
        url = reverse("get_amistats")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Ya existe una amistad en setUp
        self.assertEqual(response.data[0]["solicita"], self.user1.pk)
        self.assertEqual(response.data[0]["accepta"], self.user2.pk)

    def test_update_amistat(self):
        url = reverse("update_amistat", args=[self.amistat.pk])
        response = self.client.patch(
            url,
            {
                "solicita": self.user3.pk,
                "accepta": self.user1.pk,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Amistat.objects.get(pk=self.amistat.pk).solicita, self.user3)

    def test_delete_amistat(self):
        url = reverse("delete_amistat", args=[self.amistat.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Amistat.objects.count(), 0)


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestBloqueig(TestCase):
    def setUp(self):
        self.user1 = Usuari.objects.create(
            correu="user1@example.com",
            password="1234",
            nom="user1",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo",
            administrador=False,
        )
        self.user2 = Usuari.objects.create(
            correu="user2@example.com",
            password="1234",
            nom="user2",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo 2",
            administrador=False,
        )
        # Crear un bloqueo inicial para las pruebas de actualización y eliminación
        self.bloqueig = Bloqueig.objects.create(
            bloqueja=self.user1, bloquejat=self.user2
        )

    def test_create_bloqueig(self):
        url = reverse("create_bloqueig")
        response = self.client.post(
            url,
            {"bloqueja": self.user2.pk, "bloquejat": self.user1.pk},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Bloqueig.objects.count(), 2)  # Ya existe un bloqueo en setUp
        self.assertEqual(
            Bloqueig.objects.get(bloqueja=self.user2, bloquejat=self.user1).pk, 2
        )

    def test_get_bloqueigs(self):
        url = reverse("get_bloqueigs")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Ya existe un bloqueo en setUp
        self.assertEqual(response.data[0]["bloqueja"], self.user1.pk)
        self.assertEqual(response.data[0]["bloquejat"], self.user2.pk)

    def test_update_bloqueig(self):
        url = reverse("update_bloqueig", args=[self.bloqueig.pk])
        response = self.client.patch(
            url,
            {"bloqueja": self.user2.pk, "bloquejat": self.user1.pk},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Bloqueig.objects.get(pk=self.bloqueig.pk).bloqueja, self.user2)

    def test_delete_bloqueig(self):
        url = reverse("delete_bloqueig", args=[self.bloqueig.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Bloqueig.objects.count(), 0)


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestXat(TestCase):
    def setUp(self):
        self.user1 = Usuari.objects.create(
            correu="user1@example.com",
            password="1234",
            nom="user1",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo",
            administrador=False,
        )
        self.user2 = Usuari.objects.create(
            correu="user2@example.com",
            password="1234",
            nom="user2",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo 2",
            administrador=False,
        )
        self.xat = XatIndividual.objects.create(usuari1=self.user1, usuari2=self.user2)

    def test_create_xat(self):
        initial_count = XatIndividual.objects.count()
        url = reverse("create_xat_individual")
        response = self.client.post(
            url,
            {"usuari1": self.user2.pk, "usuari2": self.user1.pk},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(XatIndividual.objects.count(), initial_count + 1)
        xat = XatIndividual.objects.filter(
            usuari1=self.user2, usuari2=self.user1
        ).first()
        self.assertIsNotNone(xat)

    def test_get_xats(self):
        url = reverse("get_xats_individual")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Ya existe un xat en setUp
        self.assertEqual(response.data[0]["usuari1"], self.user1.pk)
        self.assertEqual(response.data[0]["usuari2"], self.user2.pk)

    def test_update_xat(self):
        url = reverse("update_xat_individual", args=[self.xat.pk])
        response = self.client.patch(
            url,
            {"usuari1": self.user1.pk, "usuari2": self.user2.pk},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_xat(self):
        url = reverse("delete_xat_individual", args=[self.xat.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(XatIndividual.objects.count(), 0)


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestXatGrupal(TestCase):
    def setUp(self):
        self.user1 = Usuari.objects.create(
            correu="user1@example.com",
            password="1234",
            nom="user1",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo",
            administrador=False,
        )
        self.user2 = Usuari.objects.create(
            correu="user2@example.com",
            password="1234",
            nom="user2",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo 2",
            administrador=False,
        )
        self.xat = XatGrupal.objects.create(
            nom="Test Chat", creador=self.user1, descripció="Test Description"
        )
        self.xat.membres.set([self.user1, self.user2])

    def test_create_xat_grupal(self):
        initial_count = XatGrupal.objects.count()
        url = reverse("create_xat_grupal")
        response = self.client.post(
            url,
            {
                "nom": "Test Chat 2",
                "creador": self.user1.pk,
                "descripció": "Test Description 2",
                "membres": [self.user1.pk, self.user2.pk],
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(XatGrupal.objects.count(), initial_count + 1)
        xat = XatGrupal.objects.get(nom="Test Chat 2")
        self.assertIsNotNone(xat)

    def test_get_xats_grupales(self):
        url = reverse("get_xats_grupal")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Ya existe un xat en setUp
        self.assertEqual(response.data[0]["creador"], self.user1.pk)
        self.assertEqual(response.data[0]["membres"], [self.user1.pk, self.user2.pk])

    def test_update_xat_grupal(self):
        url = reverse("update_xat_grupal", args=[self.xat.pk])
        response = self.client.patch(
            url,
            {"creador": self.user1.pk, "membres": [self.user2.pk]},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_xat_grupal(self):
        url = reverse("delete_xat_grupal", args=[self.xat.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(XatGrupal.objects.count(), 0)


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestInvitacio(TestCase):
    def setUp(self):
        self.user1 = Usuari.objects.create(
            correu="user1@example.com",
            password="1234",
            nom="user1",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo",
            administrador=False,
        )
        self.user2 = Usuari.objects.create(
            correu="user2@example.com",
            password="1234",
            nom="user2",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo 2",
            administrador=False,
        )
        self.xat = XatGrupal.objects.create(
            nom="Test Chat", creador=self.user1, descripció="Test Description"
        )
        self.xat.membres.set([self.user1, self.user2])
        self.invitacio = Invitacio.objects.create(
            destinatari=self.user2, creador=self.user1, xat=self.xat, estat="pendent"
        )

    def test_create_invitacio(self):
        # Crear un nuevo chat para la invitación
        xat2 = XatGrupal.objects.create(
            nom="Test Chat 2", creador=self.user1, descripció="Test Description 2"
        )
        xat2.membres.set([self.user1])

        url = reverse("create_invitacio")
        response = self.client.post(
            url,
            {
                "destinatari": self.user2.pk,
                "creador": self.user1.pk,
                "xat": xat2.pk,
                "estat": "pendent",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Invitacio.objects.count(), 2
        )  # Ya existe una invitación en setUp
        self.assertEqual(
            Invitacio.objects.get(
                destinatari=self.user2, creador=self.user1, xat=xat2
            ).pk,
            2,
        )

    def test_get_invitacions(self):
        url = reverse("get_invitacions")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Ya existe una invitación en setUp
        self.assertEqual(response.data[0]["destinatari"], self.user2.pk)
        self.assertEqual(response.data[0]["creador"], self.user1.pk)
        self.assertEqual(response.data[0]["xat"], self.xat.pk)
        self.assertEqual(response.data[0]["estat"], "pendent")

    def test_update_invitacio(self):
        url = reverse("update_invitacio", args=[self.invitacio.pk])
        response = self.client.patch(
            url,
            {"estat": "resolta"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Invitacio.objects.get(pk=self.invitacio.pk).estat, "resolta")

    def test_delete_invitacio(self):
        url = reverse("delete_invitacio", args=[self.invitacio.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Invitacio.objects.count(), 0)


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestDificultatEsportiva(TestCase):
    def setUp(self):
        self.dificultat = DificultatEsportiva.objects.create(
            nombre="Futbol", descripcio="Futbol"
        )

    def test_create_dificultat_esportiva(self):
        url = reverse("create_dificultat_esportiva")
        response = self.client.post(
            url,
            {"nombre": "Baloncesto", "descripcio": "Baloncesto"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            DificultatEsportiva.objects.count(), 2
        )  # Ya existe una dificultad en setUp
        dificultat = DificultatEsportiva.objects.get(nombre="Baloncesto")
        self.assertEqual(dificultat.nombre, "Baloncesto")

    def test_get_dificultats_esportives(self):
        url = reverse("get_dificultats_esportiva")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Ya existe una dificultad en setUp
        self.assertEqual(response.data[0]["nombre"], "Futbol")

    def test_update_dificultat_esportiva(self):
        url = reverse("update_dificultat_esportiva", args=[self.dificultat.pk])
        response = self.client.patch(
            url,
            {"nombre": "Futbol", "descripcio": "Futbol"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            DificultatEsportiva.objects.get(pk=self.dificultat.pk).nombre, "Futbol"
        )

    def test_delete_dificultat_esportiva(self):
        url = reverse("delete_dificultat_esportiva", args=[self.dificultat.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(DificultatEsportiva.objects.count(), 0)


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestAccesibilitatRespiratoria(TestCase):
    def setUp(self):
        self.accesibilitat = AccesibilitatRespiratoria.objects.create(
            nombre="Alta", descripcio="Alta"
        )

    def test_create_accesibilitat_respiratoria(self):
        url = reverse("create_accessibilitat_respiratoria")
        response = self.client.post(
            url,
            {"nombre": "Baja", "descripcio": "Baja"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            AccesibilitatRespiratoria.objects.count(), 2
        )  # Ya existe una accesibilitat en setUp
        accesibilitat = AccesibilitatRespiratoria.objects.get(nombre="Baja")
        self.assertEqual(accesibilitat.nombre, "Baja")

    def test_get_accesibilitat_respiratoria(self):
        url = reverse("get_accessibilitats_respiratoria")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Ya existe una accesibilitat en setUp
        self.assertEqual(response.data[0]["nombre"], "Alta")

    def test_update_accesibilitat_respiratoria(self):
        url = reverse(
            "update_accessibilitat_respiratoria", args=[self.accesibilitat.pk]
        )
        response = self.client.patch(
            url,
            {"nombre": "Alta", "descripcio": "Alta"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            AccesibilitatRespiratoria.objects.get(pk=self.accesibilitat.pk).nombre,
            "Alta",
        )

    def test_delete_accesibilitat_respiratoria(self):
        url = reverse(
            "delete_accessibilitat_respiratoria", args=[self.accesibilitat.pk]
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(AccesibilitatRespiratoria.objects.count(), 0)


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestRuta(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Limpiar la base de datos antes de cada test
        Ruta.objects.all().delete()
        cls.ruta = Ruta.objects.create(nom="Ruta 1", descripcio="Ruta 1", dist_km=0.0)

    def test_create_ruta(self):
        initial_count = Ruta.objects.count()
        url = reverse("create_ruta")
        response = self.client.post(
            url,
            {"nom": "Ruta 2", "descripcio": "Ruta 2", "dist_km": 0.0},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ruta.objects.count(), initial_count + 1)
        ruta = Ruta.objects.filter(nom="Ruta 2").first()
        self.assertIsNotNone(ruta)

    def test_get_rutas(self):
        url = reverse("get_rutas")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(r["nom"] == "Ruta 1" for r in response.data))

    def test_delete_ruta(self):
        initial_count = Ruta.objects.count()
        url = reverse("delete_ruta", args=[self.ruta.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Ruta.objects.count(), initial_count - 1)
        self.assertFalse(Ruta.objects.filter(pk=self.ruta.pk).exists())


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestRecompensa(TestCase):
    def setUp(self):
        self.ruta = Ruta.objects.create(nom="Ruta 1", descripcio="Ruta 1", dist_km=0.0)
        self.usuari = Usuari.objects.create(
            correu="user1@example.com",
            password="1234",
            nom="user1",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo",
            administrador=False,
        )
        self.recompensa = Recompensa.objects.create(
            usuari=self.usuari, ruta=self.ruta, data_recompensa=timezone.now(), punts=10
        )

    def test_create_recompensa(self):
        url = reverse("create_recompensa")
        response = self.client.post(
            url,
            {
                "usuari": self.usuari.pk,
                "ruta": self.ruta.pk,
                "data_recompensa": timezone.now(),
                "punts": 10,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Recompensa.objects.count(), 2
        )  # Ya existe una recompensa en setUp
        recompensa = Recompensa.objects.order_by("-id").first()
        self.assertEqual(recompensa.punts, 10)

    def test_get_recompensas(self):
        url = reverse("get_recompenses")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Ya existe una recompensa en setUp

    def test_update_recompensa(self):
        url = reverse("update_recompensa", args=[self.recompensa.pk])
        response = self.client.patch(
            url,
            {"punts": 20},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Recompensa.objects.get(pk=self.recompensa.pk).punts, 20)

    def test_delete_recompensa(self):
        url = reverse("delete_recompensa", args=[self.recompensa.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Recompensa.objects.count(), 0)


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestAssignaAccesibilitatRespiratoria(TestCase):
    def setUp(self):
        self.admin = Admin.objects.create(
            correu="admin@example.com",
            password="1234",
            nom="admin",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo",
            administrador=True,
        )
        self.accesibilitat = AccesibilitatRespiratoria.objects.create(
            nombre="Alta", descripcio="Alta"
        )
        self.ruta = Ruta.objects.create(
            nom="Test Ruta", descripcio="Test Descripcio", dist_km=10.0
        )

    def test_get_assigna_accesibilitat_respiratoria(self):
        url = reverse("get_assignacions_accesibilitat_respiratoria")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_update_assigna_accesibilitat_respiratoria(self):
        assignacio = AssignaAccesibilitatRespiratoria.objects.create(
            usuari=self.admin, accesibilitat=self.accesibilitat, ruta=self.ruta
        )
        url = reverse(
            "update_assignacio_accesibilitat_respiratoria", args=[assignacio.pk]
        )
        data = {
            "usuari": self.admin.pk,
            "accesibilitat": self.accesibilitat.pk,
            "ruta": self.ruta.pk,
        }
        response = self.client.patch(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assignacio.refresh_from_db()
        self.assertEqual(assignacio.accesibilitat, self.accesibilitat)

    def test_delete_assigna_accesibilitat_respiratoria(self):
        assignacio = AssignaAccesibilitatRespiratoria.objects.create(
            usuari=self.admin, accesibilitat=self.accesibilitat, ruta=self.ruta
        )
        url = reverse(
            "delete_assignacio_accesibilitat_respiratoria", args=[assignacio.pk]
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AssignaAccesibilitatRespiratoria.objects.count(), 0)


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestAssignaDificultatEsportiva(TestCase):
    def setUp(self):
        self.admin = Admin.objects.create(
            correu="admin@example.com",
            password="1234",
            nom="admin",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo",
            administrador=True,
        )
        self.dificultat = DificultatEsportiva.objects.create(
            nombre="Mitjana", descripcio="Mitjana"
        )
        self.ruta = Ruta.objects.create(
            nom="Test Ruta", descripcio="Test Descripcio", dist_km=10.0
        )

    def test_create_assignacio_esportiva(self):
        url = reverse("create_assignacio_esportiva")
        data = {
            "usuari": self.admin.pk,
            "ruta": self.ruta.pk,
            "dificultat": self.dificultat.pk,
        }
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AssignaDificultatEsportiva.objects.count(), 1)
        self.assertEqual(
            AssignaDificultatEsportiva.objects.first().dificultat, self.dificultat
        )

    def test_get_assignacions_esportiva(self):
        url = reverse("get_assignacions_esportiva")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_update_assignacio_esportiva(self):
        assignacio = AssignaDificultatEsportiva.objects.create(
            usuari=self.admin, dificultat=self.dificultat, ruta=self.ruta
        )
        url = reverse("update_assignacio_esportiva", args=[assignacio.pk])
        data = {
            "usuari": self.admin.pk,
            "ruta": self.ruta.pk,
            "dificultat": self.dificultat.pk,
        }
        response = self.client.patch(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assignacio.refresh_from_db()
        self.assertEqual(assignacio.dificultat, self.dificultat)

    def test_delete_assignacio_esportiva(self):
        assignacio = AssignaDificultatEsportiva.objects.create(
            usuari=self.admin, dificultat=self.dificultat, ruta=self.ruta
        )
        url = reverse("delete_assignacio_esportiva", args=[assignacio.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AssignaDificultatEsportiva.objects.count(), 0)


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestEventDeCalendari(TestCase):
    def setUp(self):
        self.event = EventDeCalendari.objects.create(
            nom="Evento 1",
            descripció="Evento 1",
            data_inici=timezone.now(),
            data_fi=timezone.now(),
        )

    def test_create_evento_calendario(self):
        url = reverse("create_event_de_calendari")
        response = self.client.post(
            url,
            {
                "nom": "Evento 2",
                "descripció": "Evento 2",
                "data_inici": timezone.now(),
                "data_fi": timezone.now(),
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            EventDeCalendari.objects.count(), 2
        )  # Ya existe un evento en setUp
        evento = EventDeCalendari.objects.get(nom="Evento 2")
        self.assertEqual(evento.descripció, "Evento 2")

    def test_get_eventos_calendario(self):
        url = reverse("get_events_de_calendari")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Ya existe un evento en setUp

    def test_update_evento_calendario(self):
        url = reverse("update_event_de_calendari", args=[self.event.pk])
        response = self.client.patch(
            url,
            {"descripció": "Evento 1 actualizado"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            EventDeCalendari.objects.get(pk=self.event.pk).descripció,
            "Evento 1 actualizado",
        )

    def test_delete_evento_calendario(self):
        url = reverse("delete_event_de_calendari", args=[self.event.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(EventDeCalendari.objects.count(), 0)


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestEventDeCalendariPrivat(TestCase):
    def setUp(self):
        self.event = EventDeCalendariPrivat.objects.create(
            nom="Evento 1",
            descripció="Evento 1",
            data_inici=timezone.now(),
            data_fi=timezone.now(),
        )

    def test_create_evento_calendario_privado(self):
        url = reverse("create_event_de_calendari_privat")
        response = self.client.post(
            url,
            {
                "nom": "Evento 2",
                "descripció": "Evento 2",
                "data_inici": timezone.now(),
                "data_fi": timezone.now(),
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(EventDeCalendariPrivat.objects.count(), 2)
        evento_privado = EventDeCalendariPrivat.objects.get(nom="Evento 2")
        self.assertEqual(evento_privado.descripció, "Evento 2")

    def test_get_eventos_calendario_privados(self):
        url = reverse("get_events_de_calendari_privats")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_update_evento_calendario_privado(self):
        url = reverse("update_event_de_calendari_privat", args=[self.event.pk])
        response = self.client.patch(
            url,
            {"descripció": "Evento 1 actualizado"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            EventDeCalendariPrivat.objects.get(pk=self.event.pk).descripció,
            "Evento 1 actualizado",
        )

    def test_delete_evento_calendario_privado(self):
        url = reverse("delete_event_de_calendari_privat", args=[self.event.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(EventDeCalendariPrivat.objects.count(), 0)


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestEventDeCalendariPublic(TestCase):
    def setUp(self):
        self.event = EventDeCalendariPublic.objects.create(
            nom="Evento 1",
            descripció="Evento 1",
            data_inici=timezone.now(),
            data_fi=timezone.now(),
            limit=10,
        )

    def test_create_evento_calendario_publico(self):
        url = reverse("create_event_de_calendari_public")
        response = self.client.post(
            url,
            {
                "nom": "Evento 2",
                "descripció": "Evento 2",
                "data_inici": timezone.now(),
                "data_fi": timezone.now(),
                "limit": 20,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(EventDeCalendariPublic.objects.count(), 2)
        evento_publico = EventDeCalendariPublic.objects.get(nom="Evento 2")
        self.assertEqual(evento_publico.descripció, "Evento 2")

    def test_get_eventos_calendario_publicos(self):
        url = reverse("get_events_de_calendari_publics")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_update_evento_calendario_publico(self):
        url = reverse("update_event_de_calendari_public", args=[self.event.pk])
        response = self.client.patch(
            url,
            {"descripció": "Evento 1 actualizado"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            EventDeCalendariPublic.objects.get(pk=self.event.pk).descripció,
            "Evento 1 actualizado",
        )

    def test_delete_evento_calendario_publico(self):
        url = reverse("delete_event_de_calendari_public", args=[self.event.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(EventDeCalendariPublic.objects.count(), 0)


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestPunt(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Limpiar la base de datos antes de cada test
        Punt.objects.all().delete()
        cls.punt = Punt.objects.create(
            latitud=1.0, longitud=1.0, index_qualitat_aire=1.0
        )

    def test_create_punt(self):
        initial_count = Punt.objects.count()
        url = reverse("create_punt")
        response = self.client.post(
            url,
            {"latitud": 2.0, "longitud": 2.0, "index_qualitat_aire": 2.0},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Punt.objects.count(), initial_count + 1)
        punt = Punt.objects.filter(latitud=2.0, longitud=2.0).first()
        self.assertIsNotNone(punt)

    def test_get_punt(self):
        url = reverse("get_punt", args=[self.punt.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["latitud"], 1.0)
        self.assertEqual(response.data["longitud"], 1.0)
        self.assertEqual(response.data["index_qualitat_aire"], 1.0)

    def test_update_punt(self):
        url = reverse("update_punt", args=[self.punt.pk])
        response = self.client.patch(
            url,
            {"latitud": 3.0},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Punt.objects.get(pk=self.punt.pk).latitud, 3.0)

    def test_delete_punt(self):
        initial_count = Punt.objects.count()
        url = reverse("delete_punt", args=[self.punt.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Punt.objects.count(), initial_count - 1)
        self.assertFalse(Punt.objects.filter(pk=self.punt.pk).exists())


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestPresencia(TestCase):
    def setUp(self):
        self.usuari = Usuari.objects.create(
            correu="user1@example.com",
            password="1234",
            nom="user1",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo",
            administrador=False,
        )
        self.punt = Punt.objects.create(
            latitud=1.0, longitud=1.0, index_qualitat_aire=1.0
        )
        self.contaminant = Contaminant.objects.create(
            nom="Contaminant 1", informacio="Información del contaminante 1"
        )
        self.presencia = Presencia.objects.create(
            punt=self.punt,
            contaminant=self.contaminant,
            data=timezone.now(),
            valor=10.0,
            valor_iqa=5.0,
        )

    def test_create_presencia(self):
        url = reverse("create_presencia")
        response = self.client.post(
            url,
            {
                "punt": self.punt.pk,
                "contaminant": self.contaminant.pk,
                "data": timezone.now(),
                "valor": 15.0,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Presencia.objects.count(), 2)
        presencia = Presencia.objects.order_by("-id").first()
        self.assertEqual(presencia.valor, 15.0)

    def test_get_presencia(self):
        url = reverse("get_presencia", args=[self.presencia.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["punt"], self.punt.pk)
        self.assertEqual(response.data["contaminant"], self.contaminant.pk)
        self.assertEqual(float(response.data["valor"]), 10.0)

    def test_update_presencia(self):
        url = reverse("update_presencia", args=[self.presencia.pk])
        response = self.client.patch(
            url,
            {"valor": 20.0},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Presencia.objects.get(pk=self.presencia.pk).valor, 20.0)

    def test_delete_presencia(self):
        initial_count = Presencia.objects.count()
        url = reverse("delete_presencia", args=[self.presencia.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Presencia.objects.count(), initial_count - 1)
        self.assertFalse(Presencia.objects.filter(pk=self.presencia.pk).exists())


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestContaminant(TestCase):
    def setUp(self):
        self.contaminant = Contaminant.objects.create(
            nom="Contaminant 1", informacio="Información del contaminante 1"
        )

    def test_create_contaminant(self):
        url = reverse("create_contaminant")
        response = self.client.post(
            url,
            {"nom": "Contaminant 2", "informacio": "Información del contaminante 2"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Contaminant.objects.count(), 2)
        contaminant = Contaminant.objects.get(nom="Contaminant 2")
        self.assertEqual(contaminant.informacio, "Información del contaminante 2")

    def test_get_contaminant(self):
        url = reverse("get_contaminant", args=[self.contaminant.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["nom"], "Contaminant 1")
        self.assertEqual(response.data["informacio"], "Información del contaminante 1")

    def test_update_contaminant(self):
        url = reverse("update_contaminant", args=[self.contaminant.pk])
        response = self.client.patch(
            url,
            {"informacio": "Información actualizada"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Contaminant.objects.get(pk=self.contaminant.pk).informacio,
            "Información actualizada",
        )

    def test_delete_contaminant(self):
        initial_count = Contaminant.objects.count()
        url = reverse("delete_contaminant", args=[self.contaminant.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Contaminant.objects.count(), initial_count - 1)
        self.assertFalse(Contaminant.objects.filter(pk=self.contaminant.pk).exists())


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestEstacioQualitatAire(TestCase):
    def setUp(self):
        self.estacio = EstacioQualitatAire.objects.create(
            nom_estacio="Estacio 1",
            descripcio="Estacio 1",
            latitud=1.0,
            longitud=1.0,
            index_qualitat_aire=1.0,
        )

    def test_create_estacio_qualitat_aire(self):
        url = reverse("create_estacio_qualitat_aire")
        response = self.client.post(
            url,
            {
                "nom_estacio": "Estacio 2",
                "descripcio": "Descripción de la estación 2",
                "latitud": 2.0,
                "longitud": 2.0,
                "index_qualitat_aire": 2.0,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(EstacioQualitatAire.objects.count(), 2)
        estacio = EstacioQualitatAire.objects.order_by("-id").first()
        self.assertEqual(estacio.descripcio, "Descripción de la estación 2")

    def test_get_estacio_qualitat_aire(self):
        url = reverse("get_estacio_qualitat_aire", args=[self.estacio.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["nom_estacio"], "Estacio 1")
        self.assertEqual(response.data["descripcio"], "Estacio 1")

    def test_update_estacio_qualitat_aire(self):
        url = reverse("update_estacio_qualitat_aire", args=[self.estacio.pk])
        response = self.client.patch(
            url,
            {"descripcio": "Descripción actualizada"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            EstacioQualitatAire.objects.get(pk=self.estacio.pk).descripcio,
            "Descripción actualizada",
        )

    def test_delete_estacio_qualitat_aire(self):
        initial_count = EstacioQualitatAire.objects.count()
        url = reverse("delete_estacio_qualitat_aire", args=[self.estacio.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(EstacioQualitatAire.objects.count(), initial_count - 1)
        self.assertFalse(
            EstacioQualitatAire.objects.filter(pk=self.estacio.pk).exists()
        )


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestActivitatCultural(TestCase):
    def setUp(self):
        self.activitat = ActivitatCultural.objects.create(
            nom_activitat="Activitat 1",
            descripcio="Descripcio de l'activitat 1",
            data_inici=timezone.now().date(),
            data_fi=timezone.now().date() + timezone.timedelta(days=1),
            latitud=1.0,
            longitud=1.0,
            index_qualitat_aire=1.0,
        )

    def test_create_activitat_cultural(self):
        url = reverse("create_activitat_cultural")
        data = {
            "nom_activitat": "Activitat 2",
            "descripcio": "Descripcio de l'activitat 2",
            "data_inici": "2025-04-24",
            "data_fi": "2025-04-25",
            "latitud": 2.0,
            "longitud": 2.0,
            "index_qualitat_aire": 2.0,
        }
        response = self.client.post(
            url,
            json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_get_activitat_cultural(self):
        url = reverse("get_activitat_cultural", args=[self.activitat.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["nom_activitat"], "Activitat 1")
        self.assertEqual(response.data["descripcio"], "Descripcio de l'activitat 1")

    def test_update_activitat_cultural(self):
        url = reverse("update_activitat_cultural", args=[self.activitat.pk])
        response = self.client.patch(
            url,
            {"descripcio": "Descripcio actualitzat"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            ActivitatCultural.objects.get(pk=self.activitat.pk).descripcio,
            "Descripcio actualitzat",
        )

    def test_delete_activitat_cultural(self):
        initial_count = ActivitatCultural.objects.count()
        url = reverse("delete_activitat_cultural", args=[self.activitat.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(ActivitatCultural.objects.count(), initial_count - 1)
        self.assertFalse(
            ActivitatCultural.objects.filter(pk=self.activitat.pk).exists()
        )


@override_settings(ROOT_URLCONF="AireLliure.urls")
class TestApuntat(TestCase):
    def setUp(self):
        self.usuari = Usuari.objects.create(
            correu="usuari1@example.com",
            password="password1",
            nom="Usuari 1",
            estat="actiu",
            punts=0,
            deshabilitador=None,
            about="hola mundo",
            administrador=False,
        )
        self.event = EventDeCalendariPublic.objects.create(
            nom="Event 1",
            descripció="Descripció de l'event 1",
            data_inici=timezone.now(),
            data_fi=timezone.now() + timezone.timedelta(hours=1),
            limit=10,
        )
        self.apuntat = Apuntat.objects.create(usuari=self.usuari, event=self.event)

    def test_create_apuntat(self):
        url = reverse("create_apuntat")
        data = {"usuari": self.usuari.pk, "event": self.event.pk}
        response = self.client.post(
            url,
            json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_get_apuntat(self):
        url = reverse("get_apuntat", args=[self.apuntat.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["usuari"], self.usuari.pk)
        self.assertEqual(response.data["event"], self.event.pk)

    def test_update_apuntat(self):
        url = reverse("update_apuntat", args=[self.apuntat.pk])
        response = self.client.patch(
            url,
            {"event": self.event.pk},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Apuntat.objects.get(pk=self.apuntat.pk).event, self.event)

    def test_delete_apuntat(self):
        initial_count = Apuntat.objects.count()
        url = reverse("delete_apuntat", args=[self.apuntat.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Apuntat.objects.count(), initial_count - 1)
        self.assertFalse(Apuntat.objects.filter(pk=self.apuntat.pk).exists())
