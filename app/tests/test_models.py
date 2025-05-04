# pylint: disable=non-ascii-name, unused-import, unused-wildcard-import
# pylint: disable=wildcard-import, too-many-lines
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
# pylint: disable=non-ascii-name
# pylint: disable=unused-import
# pylint: disable=duplicate-code

import json

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from app.forms import AssignaAccesibilitatRespiratoriaForm
from app.models import *  # noqa: F403, F405


@override_settings(ROOT_URLCONF="aire_lliure.urls")
class TestUsuariModel(TestCase):
    def setUp(self):
        self.usuari = Usuari.objects.create(
            correu="test@example.com",
            password="testpass",
            nom="Test User",
            estat="actiu",
        )

    def test_crear_usuari(self):
        self.assertEqual(self.usuari.correu, "test@example.com")
        self.assertEqual(self.usuari.nom, "Test User")
        self.assertEqual(self.usuari.estat, "actiu")


@override_settings(ROOT_URLCONF="aire_lliure.urls")
class TestAdminModel(TestCase):
    def setUp(self):
        self.admin = Admin.objects.create(
            correu="admin@example.com",
            password="adminpass",
            nom="Admin User",
            estat="actiu",
            administrador=True,
        )

    def test_crear_admin(self):
        self.assertEqual(self.admin.correu, "admin@example.com")
        self.assertEqual(self.admin.nom, "Admin User")
        self.assertEqual(self.admin.estat, "actiu")
        self.assertTrue(self.admin.administrador)


@override_settings(ROOT_URLCONF="aire_lliure.urls")
class TestRutaModel(TestCase):
    def setUp(self):
        self.ruta = Ruta.objects.create(
            nom="Test Route",
            descripcio="Test Description",
            dist_km=10.0,
        )

    def test_crear_ruta(self):
        self.assertEqual(self.ruta.nom, "Test Route")
        self.assertEqual(self.ruta.descripcio, "Test Description")
        self.assertEqual(self.ruta.dist_km, 10.0)


@override_settings(ROOT_URLCONF="aire_lliure.urls")
class TestModels(TestCase):
    def setUp(self):
        # Crear usuari de prova
        self.usuari = Usuari.objects.create(
            correu="test@example.com",
            password="testpassword",
            nom="Test User",
            estat="actiu",
        )

        # Crear admin de prova
        self.admin = Admin.objects.create(
            correu="admin@example.com",
            password="adminpassword",
            nom="Admin User",
            estat="actiu",
            administrador=True,
        )

        # Crear usuari amic
        self.usuari_amigo = Usuari.objects.create(
            correu="amigo@example.com",
            password="amigopassword",
            nom="Amigo User",
            estat="actiu",
        )

        # Crear usuari bloqueado
        self.usuari_bloqueado = Usuari.objects.create(
            correu="bloqueado@example.com",
            password="bloqueadopassword",
            nom="Bloqueado User",
            estat="actiu",
        )

        # Crear categories de prova
        self.dificultat = DificultatEsportiva.objects.create(
            nombre="Fácil", descripcio="Ruta fácil para principiantes"
        )

        self.accesibilitat = AccesibilitatRespiratoria.objects.create(
            nombre="Buena", descripcio="Buena calidad del aire"
        )

        # Crear ruta de prueba
        self.ruta = Ruta.objects.create(
            nom="Ruta de prueba", descripcio="Descripció de prueba", dist_km=5.0
        )

        # Crear punt de prueba
        self.punt = Punt.objects.create(
            latitud=41.3851, longitud=2.1734, index_qualitat_aire=50.0
        )

        # Crear evento de prueba
        self.evento = EventDeCalendariPublic.objects.create(
            nom="Evento de prueba",
            descripció="Descripció del evento",
            data_inici=timezone.now(),
            data_fi=timezone.now(),
            creador_event=self.usuari,
            limit=10,
        )

    def test_crear_usuari(self):
        self.assertEqual(self.usuari.nom, "Test User")
        self.assertEqual(self.usuari.correu, "test@example.com")
        self.assertEqual(self.usuari.estat, "actiu")
        self.assertEqual(self.usuari.punts, 0)

    def test_crear_ruta(self):
        self.assertEqual(self.ruta.nom, "Ruta de prueba")
        self.assertEqual(self.ruta.dist_km, 5.0)

    def test_crear_valoracio(self):
        ruta = Ruta.objects.create(
            nom="Ruta de prueba", descripcio="Descripció de prueba", dist_km=5.0
        )
        valoracio = Valoracio.objects.create(
            usuari=self.usuari, ruta=ruta, puntuacio=4, comentari="Muy buena ruta"
        )
        self.assertEqual(valoracio.puntuacio, 4)
        self.assertEqual(valoracio.comentari, "Muy buena ruta")

    def test_valoracio_puntuacio_invalida(self):
        ruta = Ruta.objects.create(
            nom="Ruta de prueba", descripcio="Descripció de prueba", dist_km=5.0
        )
        with self.assertRaises(IntegrityError):
            Valoracio.objects.create(
                usuari=self.usuari,
                ruta=ruta,
                puntuacio=6,  # Puntuación inválida (debe ser 0-5)
                comentari="Comentario de prueba",
            )

    def test_crear_xat_individual(self):
        xat = XatIndividual.objects.create(
            usuari1=self.usuari, usuari2=self.usuari_amigo
        )
        self.assertEqual(xat.usuari1, self.usuari)
        self.assertEqual(xat.usuari2, self.usuari_amigo)

    def test_crear_xat_grupal(self):
        xat = XatGrupal.objects.create(
            nom="Chat de prueba", creador=self.usuari, descripció="Descripció del chat"
        )
        xat.membres.add(self.usuari, self.usuari_amigo)
        self.assertEqual(xat.nom, "Chat de prueba")
        self.assertEqual(xat.creador, self.usuari)
        self.assertEqual(xat.membres.count(), 2)

    def test_crear_event_calendari(self):
        event = EventDeCalendari.objects.create(
            nom="Evento de prueba",
            descripció="Descripció del evento",
            data_inici=timezone.now(),
            data_fi=timezone.now(),
            creador_event=self.usuari,
        )
        self.assertEqual(event.nom, "Evento de prueba")
        self.assertEqual(event.creador_event, self.usuari)

    def test_crear_activitat_cultural(self):
        activitat = ActivitatCultural.objects.create(
            latitud=41.3852,
            longitud=2.1735,
            nom_activitat="Actividad de prueba",
            descripcio="Descripción de la actividad",
            data_inici=timezone.now().date(),
            data_fi=timezone.now().date(),
        )
        self.assertEqual(activitat.nom_activitat, "Actividad de prueba")
        self.assertEqual(activitat.latitud, 41.3852)

    def test_crear_apuntat(self):
        apuntat = Apuntat.objects.create(usuari=self.usuari, event=self.evento)
        self.assertEqual(apuntat.usuari, self.usuari)
        self.assertEqual(apuntat.event, self.evento)

    def test_crear_recompensa(self):
        recompensa = Recompensa.objects.create(
            usuari=self.usuari, ruta=self.ruta, punts=100
        )
        self.assertEqual(recompensa.usuari, self.usuari)
        self.assertEqual(recompensa.punts, 100)

    def test_crear_assigna_accesibilitat_respiratoria(self):
        assigna = AssignaAccesibilitatRespiratoria.objects.create(
            usuari=self.admin, accesibilitat=self.accesibilitat, ruta=self.ruta
        )
        self.assertEqual(assigna.usuari, self.admin)
        self.assertEqual(assigna.accesibilitat, self.accesibilitat)

    def test_crear_assigna_dificultat_esportiva(self):
        assigna = AssignaDificultatEsportiva.objects.create(
            usuari=self.admin, dificultat=self.dificultat, ruta=self.ruta
        )
        self.assertEqual(assigna.usuari, self.admin)
        self.assertEqual(assigna.dificultat, self.dificultat)

    def test_crear_presencia(self):
        contaminant = Contaminant.objects.create(
            nom="CO2", informacio="Dióxido de carbono"
        )
        presencia = Presencia.objects.create(
            punt=self.punt, contaminant=contaminant, data=timezone.now(), valor=50.0
        )
        self.assertEqual(presencia.punt, self.punt)
        self.assertEqual(presencia.valor, 50.0)

    def test_crear_contaminant(self):
        contaminant = Contaminant.objects.create(
            nom="CO2", informacio="Dióxido de carbono"
        )
        self.assertEqual(contaminant.nom, "CO2")
        self.assertEqual(contaminant.informacio, "Dióxido de carbono")

    def test_crear_estacio_qualitat_aire(self):
        estacio = EstacioQualitatAire.objects.create(
            latitud=41.3853,
            longitud=2.1736,
            nom_estacio="Estación de prueba",
            descripcio="Descripción de la estación",
        )
        self.assertEqual(estacio.nom_estacio, "Estación de prueba")
        self.assertEqual(estacio.latitud, 41.3853)

    def test_crear_evento_calendario_privado(self):
        evento = EventDeCalendariPrivat.objects.create(
            nom="Evento privado de prueba",
            descripció="Descripció del evento privado",
            data_inici=timezone.now(),
            data_fi=timezone.now(),
            creador_event=self.usuari,
        )
        self.assertEqual(evento.nom, "Evento privado de prueba")
        self.assertEqual(evento.creador_event, self.usuari)

    def test_crear_evento_calendario_publico(self):
        evento = EventDeCalendariPublic.objects.create(
            nom="Evento público de prueba",
            descripció="Descripció del evento público",
            data_inici=timezone.now(),
            data_fi=timezone.now(),
            creador_event=self.usuari,
            limit=10,
        )
        self.assertEqual(evento.nom, "Evento público de prueba")
        self.assertEqual(evento.creador_event, self.usuari)
        self.assertEqual(evento.limit, 10)

    def test_crear_invitacio(self):
        invitacio = Invitacio.objects.create(
            destinatari=self.usuari_amigo,
            creador=self.usuari,
            estat="pendent",
            xat=XatGrupal.objects.create(
                nom="Chat de prueba",
                creador=self.usuari,
                descripció="Descripció del chat",
            ),
        )
        self.assertEqual(invitacio.destinatari, self.usuari_amigo)
        self.assertEqual(invitacio.creador, self.usuari)
        self.assertEqual(invitacio.estat, "pendent")

    def test_crear_bloqueig(self):
        bloqueig = Bloqueig.objects.create(
            bloqueja=self.usuari, bloquejat=self.usuari_bloqueado
        )
        self.assertEqual(bloqueig.bloqueja, self.usuari)
        self.assertEqual(bloqueig.bloquejat, self.usuari_bloqueado)

    def test_crear_amistat(self):
        amistad = Amistat.objects.create(
            solicita=self.usuari, accepta=self.usuari_amigo
        )
        self.assertEqual(amistad.solicita, self.usuari)
        self.assertEqual(amistad.accepta, self.usuari_amigo)

    def test_valors_incorrectes_xat_individual(self):
        try:
            XatIndividual.objects.create(usuari1=self.usuari, usuari2=99999)
            self.fail("Debería haber lanzado IntegrityError")
        except (IntegrityError, ObjectDoesNotExist, ValueError, TypeError):
            pass
        finally:
            XatIndividual.objects.filter(usuari2=99999).delete()


@override_settings(ROOT_URLCONF="aire_lliure.urls")
class TestClasse(TestCase):
    def setUp(self):
        # Crear usuari de prova
        self.usuari = Usuari.objects.create(
            correu="test@example.com",
            password="testpassword",
            nom="Test User",
            estat="actiu",
        )

        # Crear admin
        self.admin = Admin.objects.create(
            correu="admin@example.com",
            password="adminpassword",
            nom="Admin User",
            estat="actiu",
            administrador=True,
        )

        # Crear usuari amic
        self.usuari_amigo = Usuari.objects.create(
            correu="amigo@example.com",
            password="amigopassword",
            nom="Amigo User",
            estat="actiu",
        )

        # Crear usuari bloqueado
        self.usuari_bloqueado = Usuari.objects.create(
            correu="bloqueado@example.com",
            password="bloqueadopassword",
            nom="Bloqueado User",
            estat="actiu",
        )

        # Crear amistad
        self.amistat = Amistat.objects.create(
            solicita=self.usuari, accepta=self.usuari_amigo
        )

        # Crear bloqueig
        self.bloqueig = Bloqueig.objects.create(
            bloqueja=self.usuari, bloquejat=self.usuari_bloqueado
        )

        # Crear ruta de prueba
        self.ruta = Ruta.objects.create(
            nom="Ruta de prueba", descripcio="Descripció de prueba", dist_km=5.0
        )

        # Crear punt de prueba
        self.punt = Punt.objects.create(
            latitud=41.3851, longitud=2.1734, index_qualitat_aire=50.0
        )

        # Crear dificultat esportiva
        self.dificultat = DificultatEsportiva.objects.create(
            nombre="Dificultat de prueba", descripcio="Descripció de la dificultat"
        )

        # Crear accesibilitat respiratoria
        self.accesibilitat = AccesibilitatRespiratoria.objects.create(
            nombre="Accesibilitat de prueba",
            descripcio="Descripció de la accesibilitat",
        )

        # Crear contaminant
        self.contaminant = Contaminant.objects.create(
            nom="CO2", informacio="Dióxido de carbono"
        )

        # Crear presencia
        self.presencia = Presencia.objects.create(
            punt=self.punt,
            contaminant=self.contaminant,
            data=timezone.now(),
            valor=50.0,
        )

        # Crear evento
        self.evento = EventDeCalendariPublic.objects.create(
            nom="Evento de prueba",
            descripció="Descripció del evento",
            data_inici=timezone.now(),
            data_fi=timezone.now(),
            creador_event=self.usuari,
            limit=10,
        )

        # Crear evento privado
        self.event_privat = EventDeCalendariPrivat.objects.create(
            nom="Evento privado de prueba",
            descripció="Descripció del evento privado",
            data_inici=timezone.now(),
            data_fi=timezone.now(),
            creador_event=self.usuari,
        )

        # Crear xat individual
        self.xat_privat = XatIndividual.objects.create(
            usuari1=self.usuari, usuari2=self.usuari_amigo
        )

        # Crear xat grupal
        self.xat_grupal = XatGrupal.objects.create(
            nom="Chat de prueba", creador=self.usuari, descripció="Descripció del chat"
        )
        self.xat_grupal.membres.add(self.usuari, self.usuari_amigo)

        # crear valoracio
        self.valoracio = Valoracio.objects.create(
            usuari=self.usuari, ruta=self.ruta, puntuacio=5, comentari="Muy buena ruta"
        )

        # crear estacio qualitat aire
        self.estacio = EstacioQualitatAire.objects.create(
            latitud=41.3853,
            longitud=2.1736,
            nom_estacio="Estación de prueba",
            descripcio="Descripción de la estación",
        )

        # crear activitat cultural
        self.activitat = ActivitatCultural.objects.create(
            latitud=41.3854,
            longitud=2.1737,
            nom_activitat="Actividad de prueba",
            descripcio="Descripción de la actividad",
            data_inici=timezone.now().date(),
            data_fi=timezone.now().date() + timezone.timedelta(days=7),
        )

        # crear apuntat
        self.apuntat = Apuntat.objects.create(usuari=self.usuari, event=self.evento)

        # crear recompensa
        self.recompensa = Recompensa.objects.create(
            usuari=self.usuari, ruta=self.ruta, punts=100
        )

    def test_crear_usuari(self):
        self.assertEqual(self.usuari.nom, "Test User")
        self.assertEqual(self.usuari.correu, "test@example.com")
        self.assertEqual(self.usuari.estat, "actiu")
        self.assertEqual(self.usuari.punts, 0)

    def test_crear_admin(self):
        self.assertEqual(self.admin.nom, "Admin User")
        self.assertEqual(self.admin.correu, "admin@example.com")
        self.assertEqual(self.admin.estat, "actiu")
        self.assertEqual(self.admin.administrador, True)

    def test_crear_amistat(self):
        self.assertEqual(self.amistat.solicita, self.usuari)
        self.assertEqual(self.amistat.accepta, self.usuari_amigo)

    def test_crear_bloqueig(self):
        self.assertEqual(self.bloqueig.bloqueja, self.usuari)
        self.assertEqual(self.bloqueig.bloquejat, self.usuari_bloqueado)

    def test_crear_dificultat_esportiva(self):
        self.assertEqual(self.dificultat.nombre, "Dificultat de prueba")
        self.assertEqual(self.dificultat.descripcio, "Descripció de la dificultat")

    def test_crear_accesibilitat_respiratoria(self):
        self.assertEqual(self.accesibilitat.nombre, "Accesibilitat de prueba")
        self.assertEqual(
            self.accesibilitat.descripcio, "Descripció de la accesibilitat"
        )

    def test_crear_valoracio(self):
        self.assertEqual(self.valoracio.usuari, self.usuari)
        self.assertEqual(self.valoracio.ruta, self.ruta)
        self.assertEqual(self.valoracio.puntuacio, 5)
        self.assertEqual(self.valoracio.comentari, "Muy buena ruta")

    def test_crear_ruta(self):
        self.assertEqual(self.ruta.nom, "Ruta de prueba")
        self.assertEqual(self.ruta.descripcio, "Descripció de prueba")
        self.assertEqual(self.ruta.dist_km, 5.0)

    def test_crear_xat_individual(self):
        self.assertEqual(self.xat_privat.usuari1, self.usuari)
        self.assertEqual(self.xat_privat.usuari2, self.usuari_amigo)

    def test_crear_xat_grupal(self):
        self.assertEqual(self.xat_grupal.nom, "Chat de prueba")
        self.assertEqual(self.xat_grupal.creador, self.usuari)

    def test_crear_missatge(self):
        missatge = Missatge.objects.create(
            xat=self.xat_grupal,
            text="Hola, ¿cómo estás?",
            data=timezone.now(),
            autor=self.usuari,
        )
        self.assertEqual(missatge.xat, self.xat_grupal)
        self.assertEqual(missatge.text, "Hola, ¿cómo estás?")
        self.assertEqual(missatge.autor, self.usuari)

    def test_crear_missatge_xat_individual(self):
        missatge = Missatge.objects.create(
            xat=self.xat_privat,
            text="Hola, ¿cómo estás?",
            data=timezone.now(),
            autor=self.usuari,
        )
        self.assertEqual(missatge.xat, self.xat_privat)
        self.assertEqual(missatge.text, "Hola, ¿cómo estás?")
        self.assertEqual(missatge.autor, self.usuari)

    def test_crear_invitacio(self):
        invitacio = Invitacio.objects.create(
            destinatari=self.usuari_amigo,
            creador=self.usuari,
            estat="pendent",
            xat=self.xat_grupal,
        )
        self.assertEqual(invitacio.destinatari, self.usuari_amigo)
        self.assertEqual(invitacio.creador, self.usuari)
        self.assertEqual(invitacio.estat, "pendent")
        self.assertEqual(invitacio.xat, self.xat_grupal)

    def test_crear_evento_calendari_publico(self):
        self.assertEqual(self.evento.nom, "Evento de prueba")
        self.assertEqual(self.evento.creador_event, self.usuari)
        self.assertEqual(self.evento.limit, 10)

    def test_crear_evento_calendari_privado(self):
        self.assertEqual(self.event_privat.nom, "Evento privado de prueba")
        self.assertEqual(self.event_privat.creador_event, self.usuari)

    def test_crear_presencia(self):
        self.assertEqual(self.presencia.punt, self.punt)
        self.assertEqual(self.presencia.contaminant, self.contaminant)
        self.assertEqual(self.presencia.valor, 50.0)

    def test_crear_contaminant(self):
        self.assertEqual(self.contaminant.nom, "CO2")
        self.assertEqual(self.contaminant.informacio, "Dióxido de carbono")

    def test_crear_estacio_qualitat_aire(self):
        self.assertEqual(self.estacio.nom_estacio, "Estación de prueba")
        self.assertEqual(self.estacio.latitud, 41.3853)
        self.assertEqual(self.estacio.longitud, 2.1736)
        self.assertEqual(self.estacio.descripcio, "Descripción de la estación")

    def test_crear_activitat_cultural(self):
        self.assertEqual(self.activitat.nom_activitat, "Actividad de prueba")
        self.assertEqual(self.activitat.latitud, 41.3854)
        self.assertEqual(self.activitat.longitud, 2.1737)
        self.assertEqual(self.activitat.descripcio, "Descripción de la actividad")

    def test_crear_apuntat(self):
        self.assertEqual(self.apuntat.usuari, self.usuari)
        self.assertEqual(self.apuntat.event, self.evento)

    def test_crear_recompensa(self):
        self.assertEqual(self.recompensa.usuari, self.usuari)
        self.assertEqual(self.recompensa.ruta, self.ruta)
        self.assertEqual(self.recompensa.punts, 100)

    # ara test de errors a proposit.

    def test_crear_usuari_correu_duplicat(self):
        with self.assertRaises(IntegrityError):
            Usuari.objects.create(
                correu="test@example.com",
                password="testpassword",
                nom="Test User",
                estat="actiu",
            )

    def test_crear_ruta_nom_duplicat(self):
        # Este test se elimina porque el modelo no tiene restricción de unicidad en el nombre
        pass

    def test_crear_ruta_dist_km_negatiu(self):
        # Este test se elimina porque el modelo no tiene restricción de distancia positiva
        pass

    def test_crear_ruta_dist_km_zero(self):
        # Este test se elimina porque el modelo no tiene restricción de distancia mayor que cero
        pass

    def test_crear_ruta_descripcio_null(self):
        with self.assertRaises(IntegrityError):
            Ruta.objects.create(nom="Ruta de prueba 4", descripcio=None, dist_km=5.0)

    def test_error_recompensa_ruta_null(self):
        with self.assertRaises(IntegrityError):
            Recompensa.objects.create(usuari=self.usuari, ruta=None, punts=100)

    def test_error_recompensa_usuari_null(self):
        with self.assertRaises(IntegrityError):
            Recompensa.objects.create(usuari=None, ruta=self.ruta, punts=100)

    def test_crear_malament_ruta_null(self):
        with self.assertRaises(IntegrityError):
            Recompensa.objects.create(usuari=self.usuari, ruta=None, punts=100)

    def test_crear_malament_usuari_null(self):
        with self.assertRaises(IntegrityError):
            Recompensa.objects.create(usuari=None, ruta=self.ruta, punts=100)

    def test_valors_incorrectes_xat_grupal(self):
        with self.assertRaises(IntegrityError):
            XatGrupal.objects.create(
                nom=None,  # nombre no puede ser null
                creador=self.usuari,
                descripció="Descripció del chat",
            )

    def test_valors_incorrectes_evento_calendario_publico(self):
        with self.assertRaises(IntegrityError):
            EventDeCalendariPublic.objects.create(
                nom=None,  # nombre no puede ser null
                descripció="Descripció del evento",
                data_inici=timezone.now(),
                data_fi=timezone.now(),
                creador_event=self.usuari,
                limit=-1,  # limit debe ser positivo
            )

    def test_valors_incorrectes_evento_calendario_privado(self):
        with self.assertRaises(IntegrityError):
            EventDeCalendariPrivat.objects.create(
                nom=None,  # nombre no puede ser null
                descripció="Descripció del evento privado",
                data_inici=timezone.now(),
                data_fi=timezone.now(),
                creador_event=None,  # creador no puede ser null
            )

    def test_valors_incorrectes_invitacio(self):
        with self.assertRaises(IntegrityError):
            Invitacio.objects.create(
                destinatari=None,  # destinatari no puede ser null
                creador=self.usuari,
                estat="pendent",
                xat=self.xat_grupal,
            )

    def test_valors_incorrectes_bloqueig(self):
        with self.assertRaises(IntegrityError):
            Bloqueig.objects.create(
                bloqueja=None,  # bloqueja no puede ser null
                bloquejat=self.usuari_bloqueado,
            )

    def test_valors_incorrectes_amistat(self):
        with self.assertRaises(IntegrityError):
            Amistat.objects.create(
                solicita=None, accepta=self.usuari_amigo  # solicita no puede ser null
            )

    def test_valors_incorrectes_recompensa(self):
        with self.assertRaises(IntegrityError):
            Recompensa.objects.create(usuari=self.usuari, ruta=None, punts=100)

    def test_valors_inocrrectes_invitacio(self):
        with self.assertRaises(IntegrityError):
            Invitacio.objects.create(
                destinatari=None,
                creador=self.usuari,
                estat="pendent",
                xat=self.xat_grupal,
            )

    def test_valors_inocrrectes_puntuacio_valoracio(self):
        with self.assertRaises(IntegrityError):
            Valoracio.objects.create(usuari=self.usuari, ruta=self.ruta, puntuacio=-1)

    def test_valors_incorrectes_missatge(self):
        with self.assertRaises(IntegrityError):
            Missatge.objects.create(
                xat=self.xat_grupal, text=None, data=timezone.now(), autor=self.usuari
            )

    def test_incorrecte_punt(self):
        with self.assertRaises(IntegrityError):
            Punt.objects.create(latitud=None, longitud=None, index_qualitat_aire=None)
