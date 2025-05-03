# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
# pylint: disable=non-ascii-name
# pylint: disable=unused-import
# pylint: disable=duplicate-code

from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from app.models import (
    AccesibilitatRespiratoria,
    ActivitatCultural,
    Admin,
    Amistat,
    Apuntat,
    AssignaAccesibilitatRespiratoria,
    AssignaDificultatEsportiva,
    Contaminant,
    DificultatEsportiva,
    EventDeCalendariPublic,
    Missatge,
    Presencia,
    Punt,
    Ruta,
    Usuari,
    Valoracio,
    XatGrupal,
    XatIndividual,
)


@override_settings(ROOT_URLCONF="aire_lliure.urls")
class TestJocsProva(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear usuari de prova
        self.usuari = Usuari.objects.create(
            correu="test@example.com",
            password="testpass",
            nom="Test User",
            estat="actiu",
        )

        # Crear admin de prova
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

        # Crear usuaris base per tots els jocs de prova
        self.usuari1 = Usuari.objects.create(
            correu="usuari1@example.com",
            password="pass123",
            nom="Usuari 1",
            estat="actiu",
        )

        self.usuari2 = Usuari.objects.create(
            correu="usuari2@example.com",
            password="pass123",
            nom="Usuari 2",
            estat="actiu",
        )

    def test_joc_prova_rutes_i_valoracions(self):
        """Joc de prova per provar rutes i les seves valoracions"""
        # Crear rutes
        ruta1 = Ruta.objects.create(
            nom="Ruta del Montseny", descripcio="Ruta per la muntanya", dist_km=10.5
        )

        ruta2 = Ruta.objects.create(
            nom="Ruta de la Costa", descripcio="Ruta per la costa", dist_km=5.2
        )

        # Crear valoracions
        Valoracio.objects.create(
            usuari=self.usuari1, ruta=ruta1, puntuacio=5, comentari="Excel·lent ruta!"
        )

        Valoracio.objects.create(
            usuari=self.usuari2, ruta=ruta1, puntuacio=4, comentari="Molt bona ruta"
        )

        Valoracio.objects.create(
            usuari=self.usuari1, ruta=ruta2, puntuacio=3, comentari="Ruta normal"
        )

        # Verificacions
        self.assertEqual(Ruta.objects.count(), 3)  # 2 rutes noves + 1 del setUp
        self.assertEqual(Valoracio.objects.count(), 3)

        # Verificar valoracions de ruta1
        valoracions_ruta1 = Valoracio.objects.filter(ruta=ruta1)
        self.assertEqual(valoracions_ruta1.count(), 2)
        self.assertEqual(valoracions_ruta1[0].puntuacio, 5)
        self.assertEqual(valoracions_ruta1[1].puntuacio, 4)

        # Verificar valoracions de ruta2
        valoracions_ruta2 = Valoracio.objects.filter(ruta=ruta2)
        self.assertEqual(valoracions_ruta2.count(), 1)
        self.assertEqual(valoracions_ruta2[0].puntuacio, 3)

    def test_joc_prova_events_i_apuntats(self):
        """Joc de prova per provar events i apuntats"""
        # Crear events
        event1 = EventDeCalendariPublic.objects.create(
            nom="Festival de Música",
            descripció="Gran festival de música",
            data_inici=timezone.now(),
            data_fi=timezone.now() + timezone.timedelta(days=3),
            limit=100,
        )

        event2 = EventDeCalendariPublic.objects.create(
            nom="Cursa Popular",
            descripció="Cursa per la ciutat",
            data_inici=timezone.now() + timezone.timedelta(days=7),
            data_fi=timezone.now() + timezone.timedelta(days=7, hours=2),
            limit=50,
        )

        # Crear apuntats
        Apuntat.objects.create(event=event1, usuari=self.usuari1)
        Apuntat.objects.create(event=event1, usuari=self.usuari2)
        Apuntat.objects.create(event=event2, usuari=self.usuari1)

        # Verificacions
        self.assertEqual(EventDeCalendariPublic.objects.count(), 2)
        self.assertEqual(Apuntat.objects.count(), 3)

        # Verificar apuntats a event1
        apuntats_event1 = Apuntat.objects.filter(event=event1)
        self.assertEqual(apuntats_event1.count(), 2)
        self.assertTrue(apuntats_event1.filter(usuari=self.usuari1).exists())
        self.assertTrue(apuntats_event1.filter(usuari=self.usuari2).exists())

        # Verificar apuntats a event2
        apuntats_event2 = Apuntat.objects.filter(event=event2)
        self.assertEqual(apuntats_event2.count(), 1)
        self.assertTrue(apuntats_event2.filter(usuari=self.usuari1).exists())

    def test_joc_prova_xats_i_missatges(self):
        """Joc de prova per provar xats i missatges"""
        # Crear xat individual
        xat_individual = XatIndividual.objects.create(
            usuari1=self.usuari1, usuari2=self.usuari2
        )

        # Crear xat grupal
        xat_grupal = XatGrupal.objects.create(
            nom="Xat de Rutes",
            creador=self.usuari1,
            descripció="Xat per compartir rutes",
        )
        xat_grupal.membres.add(self.usuari1, self.usuari2)

        # Crear missatges
        Missatge.objects.create(
            text="Hola, com estàs?", xat=xat_individual, autor=self.usuari1
        )

        Missatge.objects.create(
            text="Molt bé, gràcies!", xat=xat_individual, autor=self.usuari2
        )

        Missatge.objects.create(
            text="Hola a tothom!", xat=xat_grupal, autor=self.usuari1
        )

        # Verificacions
        self.assertEqual(XatIndividual.objects.count(), 1)
        self.assertEqual(XatGrupal.objects.count(), 1)
        self.assertEqual(Missatge.objects.count(), 3)

        # Verificar membres del xat grupal
        self.assertEqual(xat_grupal.membres.count(), 2)
        self.assertTrue(xat_grupal.membres.filter(correu=self.usuari1.correu).exists())
        self.assertTrue(xat_grupal.membres.filter(correu=self.usuari2.correu).exists())

        # Verificar missatges del xat individual
        missatges_individual = Missatge.objects.filter(xat=xat_individual).order_by(
            "id"
        )
        self.assertEqual(missatges_individual.count(), 2)
        self.assertEqual(missatges_individual[0].text, "Hola, com estàs?")
        self.assertEqual(missatges_individual[1].text, "Molt bé, gràcies!")

        # Verificar missatges del xat grupal
        missatges_grupal = Missatge.objects.filter(xat=xat_grupal)
        self.assertEqual(missatges_grupal.count(), 1)
        self.assertEqual(missatges_grupal[0].text, "Hola a tothom!")

    def test_joc_prova_qualitat_aire(self):
        """Joc de prova per provar la qualitat de l'aire"""
        # Crear punts de mesura
        punt1 = Punt.objects.create(
            latitud=41.3851, longitud=2.1734, index_qualitat_aire=75.0
        )

        punt2 = Punt.objects.create(
            latitud=41.3900, longitud=2.1800, index_qualitat_aire=85.0
        )

        # Crear contaminants
        co2 = Contaminant.objects.create(nom="CO2", informacio="Diòxid de carboni")
        no2 = Contaminant.objects.create(nom="NO2", informacio="Diòxid de nitrogen")

        # Crear presències
        Presencia.objects.create(
            punt=punt1, contaminant=co2, data=timezone.now(), valor=25.5, valor_iqa=75.0
        )

        Presencia.objects.create(
            punt=punt2, contaminant=no2, data=timezone.now(), valor=15.0, valor_iqa=85.0
        )

        # Verificacions
        self.assertEqual(Punt.objects.count(), 2)
        self.assertEqual(Contaminant.objects.count(), 2)
        self.assertEqual(Presencia.objects.count(), 2)

        # Verificar presències del punt1
        presencies_punt1 = Presencia.objects.filter(punt=punt1)
        self.assertEqual(presencies_punt1.count(), 1)
        self.assertEqual(presencies_punt1[0].valor, 25.5)
        self.assertEqual(presencies_punt1[0].valor_iqa, 75.0)
        self.assertEqual(presencies_punt1[0].contaminant, co2)

        # Verificar presències del punt2
        presencies_punt2 = Presencia.objects.filter(punt=punt2)
        self.assertEqual(presencies_punt2.count(), 1)
        self.assertEqual(presencies_punt2[0].valor, 15.0)
        self.assertEqual(presencies_punt2[0].valor_iqa, 85.0)
        self.assertEqual(presencies_punt2[0].contaminant, no2)

    def test_joc_prova_activitats_culturals(self):
        """Joc de prova per provar activitats culturals"""
        # Crear activitats
        activitat1 = ActivitatCultural.objects.create(
            nom_activitat="Festival de Jazz",
            descripcio="Festival de jazz al parc",
            data_inici=timezone.now().date(),
            data_fi=(timezone.now() + timezone.timedelta(days=2)).date(),
            latitud=41.3851,
            longitud=2.1734,
            index_qualitat_aire=80.0,
        )

        activitat2 = ActivitatCultural.objects.create(
            nom_activitat="Teatre al Carrer",
            descripcio="Representació teatral",
            data_inici=(timezone.now() + timezone.timedelta(days=5)).date(),
            data_fi=(timezone.now() + timezone.timedelta(days=5)).date(),
            latitud=41.3900,
            longitud=2.1800,
            index_qualitat_aire=85.0,
        )

        # Verificacions
        self.assertEqual(ActivitatCultural.objects.count(), 2)

        # Verificar activitat1
        self.assertEqual(activitat1.nom_activitat, "Festival de Jazz")
        self.assertEqual(activitat1.index_qualitat_aire, 80.0)
        self.assertEqual(
            activitat1.data_fi - activitat1.data_inici, timezone.timedelta(days=2)
        )

        # Verificar activitat2
        self.assertEqual(activitat2.nom_activitat, "Teatre al Carrer")
        self.assertEqual(activitat2.index_qualitat_aire, 85.0)
        self.assertEqual(activitat2.data_fi, activitat2.data_inici)

    def test_joc_prova_ranking_i_amistats(self):
        """Joc de prova per provar el sistema de ranking i amistats"""
        # Crear més usuaris
        usuari3 = Usuari.objects.create(
            correu="usuari3@example.com",
            password="pass123",
            nom="Usuari 3",
            estat="actiu",
            punts=150,
        )

        usuari4 = Usuari.objects.create(
            correu="usuari4@example.com",
            password="pass123",
            nom="Usuari 4",
            estat="actiu",
            punts=200,
        )

        # Assignar punts
        self.usuari1.punts = 300
        self.usuari1.save()

        self.usuari2.punts = 100
        self.usuari2.save()

        # Crear amistats
        Amistat.objects.create(
            solicita=self.usuari1, accepta=self.usuari2, pendent=False
        )

        Amistat.objects.create(solicita=self.usuari1, accepta=usuari3, pendent=False)

        Amistat.objects.create(solicita=self.usuari1, accepta=usuari4, pendent=False)

        # Verificacions
        self.assertEqual(
            Usuari.objects.filter(estat="actiu", administrador=False).count(), 5
        )  # 4 usuaris nous + 1 del setUp
        self.assertEqual(Amistat.objects.count(), 3)

        # Verificar punts dels usuaris
        self.assertEqual(self.usuari1.punts, 300)
        self.assertEqual(self.usuari2.punts, 100)
        self.assertEqual(usuari3.punts, 150)
        self.assertEqual(usuari4.punts, 200)

        # Verificar amistats de l'usuari1
        amistats_usuari1 = Amistat.objects.filter(solicita=self.usuari1)
        self.assertEqual(amistats_usuari1.count(), 3)
        self.assertTrue(amistats_usuari1.filter(accepta=self.usuari2).exists())
        self.assertTrue(amistats_usuari1.filter(accepta=usuari3).exists())
        self.assertTrue(amistats_usuari1.filter(accepta=usuari4).exists())

    def test_joc_prova_dificultats_i_accesibilitat(self):
        """Joc de prova per provardifficulties i accesibilitat"""
        # Creardifficulties
        dificultat1 = DificultatEsportiva.objects.create(
            nombre="Fàcil", descripcio="Ruta fàcil per a principiants"
        )

        dificultat2 = DificultatEsportiva.objects.create(
            nombre="Mitjà", descripcio="Ruta amb algunadifficulties"
        )

        # Crear accesibilitats
        accesibilitat1 = AccesibilitatRespiratoria.objects.create(
            nombre="Bona", descripcio="Aire net i fresc"
        )

        accesibilitat2 = AccesibilitatRespiratoria.objects.create(
            nombre="Regular", descripcio="Aire amb alguna contaminació"
        )

        # Crear rutes
        ruta1 = Ruta.objects.create(
            nom="Ruta Fàcil", descripcio="Ruta per a principiants", dist_km=3.0
        )

        ruta2 = Ruta.objects.create(
            nom="Ruta Mitjana", descripcio="Ruta amb algunadifficulties", dist_km=7.0
        )

        # Assignardifficulties i accesibilitats
        AssignaDificultatEsportiva.objects.create(
            usuari=self.admin, dificultat=dificultat1, ruta=ruta1
        )

        AssignaDificultatEsportiva.objects.create(
            usuari=self.admin, dificultat=dificultat2, ruta=ruta2
        )

        AssignaAccesibilitatRespiratoria.objects.create(
            usuari=self.admin, accesibilitat=accesibilitat1, ruta=ruta1
        )

        AssignaAccesibilitatRespiratoria.objects.create(
            usuari=self.admin, accesibilitat=accesibilitat2, ruta=ruta2
        )

        # Verificacions
        self.assertEqual(DificultatEsportiva.objects.count(), 2)
        self.assertEqual(AccesibilitatRespiratoria.objects.count(), 2)
        self.assertEqual(Ruta.objects.count(), 3)  # 2 rutes noves + 1 del setUp
        self.assertEqual(AssignaDificultatEsportiva.objects.count(), 2)
        self.assertEqual(AssignaAccesibilitatRespiratoria.objects.count(), 2)

        # Verificar assignacions de ruta1
        assignacions_ruta1 = AssignaDificultatEsportiva.objects.filter(ruta=ruta1)
        self.assertEqual(assignacions_ruta1.count(), 1)
        self.assertEqual(assignacions_ruta1[0].dificultat, dificultat1)

        accesibilitats_ruta1 = AssignaAccesibilitatRespiratoria.objects.filter(
            ruta=ruta1
        )
        self.assertEqual(accesibilitats_ruta1.count(), 1)
        self.assertEqual(accesibilitats_ruta1[0].accesibilitat, accesibilitat1)

        # Verificar assignacions de ruta2
        assignacions_ruta2 = AssignaDificultatEsportiva.objects.filter(ruta=ruta2)
        self.assertEqual(assignacions_ruta2.count(), 1)
        self.assertEqual(assignacions_ruta2[0].dificultat, dificultat2)

        accesibilitats_ruta2 = AssignaAccesibilitatRespiratoria.objects.filter(
            ruta=ruta2
        )
        self.assertEqual(accesibilitats_ruta2.count(), 1)
        self.assertEqual(accesibilitats_ruta2[0].accesibilitat, accesibilitat2)
