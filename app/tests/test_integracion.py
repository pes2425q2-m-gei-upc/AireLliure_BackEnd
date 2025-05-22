# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
# pylint: disable=non-ascii-name
# pylint: disable=unused-import
# pylint: disable=duplicate-code

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from app.models import (
    AccesibilitatRespiratoria,
    ActivitatCultural,
    Admin,
    Amistat,
    Apuntat,
    AssignaAccesibilitatRespiratoria,
    Contaminant,
    DificultatEsportiva,
    EstacioQualitatAire,
    EventDeCalendariPrivat,
    EventDeCalendariPublic,
    Missatge,
    Presencia,
    Punt,
    Recompensa,
    Ruta,
    Usuari,
    Valoracio,
    XatGrupal,
    XatIndividual,
)


@override_settings(ROOT_URLCONF="aire_lliure.urls")
class TestIntegracion(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear usuari de prova
        self.usuari = Usuari.objects.create(
            correu="test@example.com",
            password="testpass",
            nom="Test User",
            estat="actiu",
        )

        self.usuari2 = Usuari.objects.create(
            correu="test2@example.com",
            password="testpassword",
            nom="Test User 2",
            estat="actiu",
        )

        self.admin = Admin.objects.create(
            correu="admin@example.com",
            password="adminpass",
            nom="Admin User",
            estat="actiu",
            administrador=True,
        )

        # Crear ruta de prova
        self.ruta = Ruta.objects.create(
            nom="Ruta de prueba", descripcio="Descripcion de prueba", dist_km=5.0
        )

    def test_flujo_completo_ruta_y_valoracion(self):
        # 1. Crear ruta
        url = reverse("create_ruta")
        data = {
            "nom": "Ruta de prueba valoracion",
            "descripcio": "Descripcion de prueba",
            "dist_km": 5.0,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ruta_id = response.data["id"]  # Obtenemos el ID de la ruta creada
        ruta = Ruta.objects.get(id=ruta_id)

        # 2. Crear valoració
        url = reverse("create_valoracio")
        data = {
            "usuari": self.usuari.correu,
            "ruta": ruta.id,
            "puntuacio": 4,
            "comentari": "Molt bona ruta",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 3. Verificar valoració
        valoracio = Valoracio.objects.get(usuari=self.usuari, ruta=ruta)
        self.assertEqual(valoracio.puntuacio, 4)
        self.assertEqual(valoracio.comentari, "Molt bona ruta")

    def test_flujo_completo_evento_y_apuntarse(self):
        # 1. Crear event públic
        url = reverse("create_event_de_calendari_public")
        data = {
            "nom": "Event de prueba",
            "descripció": "Descripció de l'event",
            "data_inici": timezone.now(),
            "data_fi": timezone.now(),
            "creador": self.usuari.correu,
            "limit": 10,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        evento = EventDeCalendariPublic.objects.get(nom="Event de prueba")

        # 2. Apuntar-se a l'event
        url = reverse("create_apuntat")
        data = {"event": evento.id, "usuari": self.usuari2.correu}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 3. Verificar apuntat
        apuntat = Apuntat.objects.get(event=evento, usuari=self.usuari2)
        self.assertIsNotNone(apuntat)

    def test_flujo_completo_bloqueo_y_amistad(self):
        # 1. Crear amistat
        amistat = Amistat.objects.create(
            solicita=self.usuari, accepta=self.usuari2, pendent=False
        )

        # 2. Crear bloqueig
        url = reverse("create_bloqueig")
        data = {"bloqueja": self.usuari.correu, "bloquejat": self.usuari2.correu}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 3. Verificar que l'amistat s'ha eliminat
        with self.assertRaises(Amistat.DoesNotExist):
            Amistat.objects.get(id=amistat.id)

    def test_flujo_completo_recompensa_y_puntos(self):
        # 1. Crear ruta
        ruta = Ruta.objects.create(
            nom="Ruta de prueba recompensa",
            descripcio="Descripcion de prueba",
            dist_km=5.0,
        )

        # 2. Crear recompensa
        url = reverse("create_recompensa")
        data = {"usuari": self.usuari.correu, "ruta": ruta.id, "punts": 100}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 3. Verificar punts actualitzats
        self.usuari.refresh_from_db()
        self.assertEqual(self.usuari.punts, 100)

        # 4. Eliminar recompensa i verificar punts
        recompensa = Recompensa.objects.get(usuari=self.usuari, ruta=ruta)
        url = reverse("delete_recompensa", args=[recompensa.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.usuari.refresh_from_db()
        self.assertEqual(self.usuari.punts, 0)

    def test_flujo_completo_dificultat_y_accesibilitat(self):
        # 1. Crear dificultat i accesibilitat
        dificultat = DificultatEsportiva.objects.create(
            nombre="Fàcil", descripcio="Ruta fàcil per a principiants"
        )

        accesibilitat = AccesibilitatRespiratoria.objects.create(
            nombre="Bona", descripcio="Aire net i fresc"
        )

        # 2. Crear ruta
        ruta = Ruta.objects.create(
            nom="Ruta de prueba dificultad",
            descripcio="Descripcion de prueba",
            dist_km=5.0,
        )

        # 3. Assignar dificultat
        url = reverse("create_assignacio_esportiva")
        data = {
            "usuari": self.admin.correu,
            "dificultat": dificultat.nombre,
            "ruta": ruta.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 4. Assignar accesibilitat directament
        assignacio = AssignaAccesibilitatRespiratoria.objects.create(
            usuari=self.admin, accesibilitat=accesibilitat, ruta=ruta
        )
        self.assertIsNotNone(assignacio)  # Verificar que s'ha creat l'assignació

    def test_flujo_completo_xat_grupal_y_invitacion(self):
        # 1. Crear xat grupal
        url = reverse("create_xat_grupal")
        data = {
            "nom": "Xat de prueba",
            "creador": self.usuari.correu,
            "descripció": "Descripció del xat",
            "membres": [self.usuari.correu],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        xat = XatGrupal.objects.get(nom="Xat de prueba")

        # 2. Crear invitació
        url = reverse("create_invitacio")
        data = {
            "destinatari": self.usuari2.correu,
            "creador": self.usuari.correu,
            "estat": "pendent",
            "xat": xat.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 3. Afegir usuari al xat
        url = reverse("afegir_usuari_xat", args=[xat.id, self.usuari2.correu])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 4. Verificar que l'usuari està al xat
        self.assertTrue(xat.membres.filter(correu=self.usuari2.correu).exists())

    def test_flujo_completo_evento_privado_y_mensajes(self):
        # 1. Crear xat individual
        xat = XatIndividual.objects.create(usuari1=self.usuari, usuari2=self.usuari2)

        # 2. Crear event privat
        url = reverse("create_event_de_calendari_privat")
        data = {
            "nom": "Event privat",
            "descripció": "Descripció de l'event privat",
            "data_inici": timezone.now(),
            "data_fi": timezone.now(),
            "creador": self.usuari.correu,
            "xat": xat.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        evento = EventDeCalendariPrivat.objects.get(nom="Event privat")
        self.assertIsNotNone(evento)  # Verificar que l'event existeix

        # 3. Enviar missatge sobre l'event
        url = reverse("create_missatge")
        data = {
            "text": "T'apuntes a l'event?",
            "xat": xat.id,
            "autor": self.usuari.correu,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 4. Verificar missatge
        missatge = Missatge.objects.get(xat=xat)
        self.assertEqual(missatge.text, "T'apuntes a l'event?")

    def test_flujo_completo_activitat_cultural_y_presencia(self):
        # 1. Crear punt amb coordenades úniques
        punt = Punt.objects.create(
            latitud=41.3851, longitud=2.1734, index_qualitat_aire=75.0
        )

        # 2. Crear activitat cultural amb coordenades diferents
        activitat = ActivitatCultural.objects.create(
            nom_activitat="Festival de música",
            descripcio="Festival de música a l'aire lliure",
            data_inici=timezone.now().date(),
            data_fi=(timezone.now() + timezone.timedelta(days=3)).date(),
            latitud=41.3852,
            longitud=2.1735,
            index_qualitat_aire=75.0,
        )
        self.assertIsNotNone(activitat)  # Verificar que l'activitat existeix

        # 3. Crear contaminant
        contaminant = Contaminant.objects.create(
            nom="NO2", informacio="Diòxid de nitrogen"
        )

        # 4. Crear presència directament
        presencia = Presencia.objects.create(
            punt=punt,
            contaminant=contaminant,
            data=timezone.now(),
            valor=25.5,
            valor_iqa=75.0,
        )

        # 5. Verificar presència
        presencia = Presencia.objects.get(punt=punt, contaminant=contaminant)
        self.assertEqual(presencia.valor, 25.5)
        self.assertEqual(presencia.valor_iqa, 75.0)

    def test_flujo_completo_estacio_qualitat_aire(self):
        # 1. Crear estació amb coordenades úniques
        estacio = EstacioQualitatAire.objects.create(
            nom_estacio="Estació Central",
            descripcio="Estació de mesura central",
            latitud=41.3853,
            longitud=2.1736,
            index_qualitat_aire=80.0,
        )

        # 2. Crear contaminant
        contaminant = Contaminant.objects.create(nom="O3", informacio="Ozó")

        # 3. Crear mesura directament
        presencia = Presencia.objects.create(
            punt=estacio,
            contaminant=contaminant,
            data=timezone.now(),
            valor=45.0,
            valor_iqa=85.0,
        )

        # 4. Verificar mesura
        presencia = Presencia.objects.get(punt=estacio, contaminant=contaminant)
        self.assertEqual(presencia.valor, 45.0)
        self.assertEqual(presencia.valor_iqa, 85.0)

    def test_flujo_completo_ranking_y_amistades(self):
        # 1. Crear diferents usuaris amb diferents punts
        usuari3 = Usuari.objects.create(
            correu="test3@example.com",
            password="testpassword",
            nom="Test User 3",
            estat="actiu",
            punts=150,
        )

        self.usuari.punts = 200
        self.usuari.save()

        self.usuari2.punts = 100
        self.usuari2.save()

        # 2. Crear amistats
        Amistat.objects.create(
            solicita=self.usuari, accepta=self.usuari2, pendent=False
        )

        Amistat.objects.create(solicita=self.usuari, accepta=usuari3, pendent=False)

        # 3. Obtenir ranking general
        url = reverse("obtenir_ranking_usuaris_all")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ranking_general = response.data
        self.assertEqual(ranking_general[0]["correu"], self.usuari.correu)

        # 4. Obtenir ranking d'amics
        url = reverse("obtenir_ranking_usuari_amics", args=[self.usuari.correu])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ranking_amics = response.data
        self.assertEqual(len(ranking_amics), 3)  # Inclou l'usuari i els seus dos amics

    def test_flujo_completo_evento_y_actualizacion(self):
        # 1. Crear event públic
        url = reverse("create_event_de_calendari_public")
        data = {
            "nom": "Event de prueba",
            "descripció": "Descripció de l'event",
            "data_inici": timezone.now(),
            "data_fi": timezone.now(),
            "creador": self.usuari.correu,
            "limit": 10,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        evento = EventDeCalendariPublic.objects.get(nom="Event de prueba")

        # 2. Actualitzar event
        url = reverse("update_event_de_calendari_public", args=[evento.id])
        data = {"nom": "Event actualitzat", "limit": 15}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        evento.refresh_from_db()
        self.assertEqual(evento.nom, "Event actualitzat")
        self.assertEqual(evento.limit, 15)

        # 3. Eliminar event
        url = reverse("delete_event_de_calendari_public", args=[evento.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(EventDeCalendariPublic.DoesNotExist):
            EventDeCalendariPublic.objects.get(id=evento.id)

    def test_flujo_completo_ruta_y_valoraciones(self):
        # 1. Crear ruta
        ruta = Ruta.objects.create(
            nom="Ruta de prueba valoraciones",
            descripcio="Descripcion de prueba",
            dist_km=5.0,
        )

        # 2. Crear valoració
        valoracio = Valoracio.objects.create(
            usuari=self.usuari, ruta=ruta, puntuacio=4, comentari="Molt bona ruta"
        )

        # 3. Actualitzar valoració
        url = reverse("update_valoracio", args=[valoracio.id])
        data = {"puntuacio": 5, "comentari": "Excel·lent ruta"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        valoracio.refresh_from_db()
        self.assertEqual(valoracio.puntuacio, 5)
        self.assertEqual(valoracio.comentari, "Excel·lent ruta")

        # 4. Eliminar valoració
        url = reverse("delete_valoracio", args=[valoracio.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Valoracio.DoesNotExist):
            Valoracio.objects.get(id=valoracio.id)

    def test_flujo_completo_chat_grupal_y_mensajes(self):
        # 1. Crear xat grupal
        xat = XatGrupal.objects.create(
            nom="Xat de prueba", creador=self.usuari, descripció="Descripció del xat"
        )
        xat.membres.add(self.usuari, self.usuari2)

        # 2. Enviar missatge
        missatge = Missatge.objects.create(
            text="Hola a tothom", xat=xat, autor=self.usuari
        )

        # 3. Actualitzar missatge
        url = reverse("update_missatge", args=[missatge.id])
        data = {"text": "Hola a tothom, com esteu?"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        missatge.refresh_from_db()
        self.assertEqual(missatge.text, "Hola a tothom, com esteu?")

        # 4. Eliminar missatge
        url = reverse("delete_missatge", args=[missatge.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Missatge.DoesNotExist):
            Missatge.objects.get(id=missatge.id)

    def test_flujo_completo_contaminante_y_presencia(self):
        # 1. Crear contaminant
        contaminant = Contaminant.objects.create(
            nom="CO2", informacio="Diòxid de carboni"
        )

        # 2. Crear punt
        punt = Punt.objects.create(
            latitud=41.3851, longitud=2.1734, index_qualitat_aire=80.0
        )

        # 3. Crear presència
        presencia = Presencia.objects.create(
            punt=punt,
            contaminant=contaminant,
            data=timezone.now(),
            valor=30.0,
            valor_iqa=80.0,
        )

        # 4. Actualitzar presència
        url = reverse("update_presencia", args=[presencia.id])
        data = {"valor": 35.0, "valor_iqa": 85.0}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        presencia.refresh_from_db()
        self.assertEqual(presencia.valor, 35.0)
        self.assertEqual(presencia.valor_iqa, 85.0)

        # 5. Eliminar presència
        url = reverse("delete_presencia", args=[presencia.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Presencia.DoesNotExist):
            Presencia.objects.get(id=presencia.id)

    def test_error_crear_event_sense_permisos(self):
        # 1. Crear event públic amb usuari normal
        url = reverse("create_event_de_calendari_public")
        data = {
            "nom": "Event de prueba",
            "descripció": "Descripció de l'event",
            "data_inici": timezone.now(),
            "data_fi": timezone.now(),
            "creador": self.usuari2.correu,  # Usuari normal, no admin
            "limit": 10,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2. Verificar que s'ha creat l'event
        evento = EventDeCalendariPublic.objects.get(nom="Event de prueba")
        self.assertIsNotNone(evento)

    def test_error_crear_valoracio_amb_puntuacio_invalida(self):
        # 1. Crear ruta
        ruta = Ruta.objects.create(
            nom="Ruta de prueba puntuacion invalida",
            descripcio="Descripcion de prueba",
            dist_km=5.0,
        )

        # 2. Intentar crear valoració amb puntuació invàlida
        url = reverse("create_valoracio")
        data = {
            "usuari": self.usuari.correu,
            "ruta": ruta.id,
            "puntuacio": 6,  # Puntuació màxima hauria de ser 5
            "comentari": "Molt bona ruta",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 3. Verificar que no s'ha creat la valoració
        with self.assertRaises(Valoracio.DoesNotExist):
            Valoracio.objects.get(usuari=self.usuari, ruta=ruta)

    def test_error_crear_presencia_amb_valors_invalids(self):
        # 1. Crear punt
        punt = Punt.objects.create(
            latitud=41.3851, longitud=2.1734, index_qualitat_aire=80.0
        )

        # 2. Crear contaminant
        contaminant = Contaminant.objects.create(
            nom="CO2", informacio="Diòxid de carboni"
        )

        # 3. Intentar crear presència amb valors invàlids
        url = reverse("create_presencia")
        data = {
            "punt": punt.id,
            "contaminant": contaminant.id,
            "data": timezone.now(),
            "valor": -10.0,  # Valor negatiu no vàlid
            "valor_iqa": 150.0,  # IQA fora del rang vàlid
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 4. Verificar que no s'ha creat la presència
        with self.assertRaises(Presencia.DoesNotExist):
            Presencia.objects.get(punt=punt, contaminant=contaminant)

    def test_error_crear_xat_grupal_sense_membres(self):
        # 1. Intentar crear xat grupal sense membres
        url = reverse("create_xat_grupal")
        data = {
            "nom": "Xat de prueba",
            "creador": self.usuari.correu,
            "descripció": "Descripció del xat",
            "membres": [],  # Llista buida de membres
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 2. Verificar que no s'ha creat el xat
        with self.assertRaises(XatGrupal.DoesNotExist):
            XatGrupal.objects.get(nom="Xat de prueba")
