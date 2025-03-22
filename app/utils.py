import requests
import uuid
from django.utils.timezone import now, timedelta
from .models import JobExecution, Presencia, Contaminant, Ruta, Punt, EstacioQualitatAire, ActivitatCultural
from django.db import transaction
from rest_framework.exceptions import ValidationError
from app.serializers import PresenciaSerializer, RutaSerializer, ContaminantSerializer, PuntSerializer, EstacioQualitatAireSerializer, ActivitatCulturalSerializer

OPEN_DATA_BCN_URL = "https://opendata-ajuntament.barcelona.cat/data/dataset/8f9f4b41-3260-4009-b6a2-80c9810776be/resource/d594937a-1ed0-4f08-8902-8bff2fcbd8b1/download"
DADES_OBERTES_DE_LA_GENERALITAT_URL = "https://analisi.transparenciacatalunya.cat/resource/tasf-thgu.json" #"?$select=nom_estacio,altitud,latitud,longitud,contaminant,data,magnitud"
SERVEI_ACTIVITATS_CULTURALS_URL = "https://???"

def genera_ruta_id(register_id) -> int:
    return register_id % (2**31)

def actualitzar_rutes():
    job, created = JobExecution.objects.get_or_create(name="actualizar_rutas")
    if created or now() - job.last_run >= timedelta(weeks=1):

        response = requests.get(OPEN_DATA_BCN_URL)
        if response.status_code == 200:
            dades = response.json()
            dades_punts = {}
            dades_rutes = []

            for ruta_info in dades:
                ruta_id = genera_ruta_id(ruta_info.get("register_id"))
                ruta_nombre = ruta_info.get("name")
                ruta_descripcio = ruta_info.get("body")
                latitud = ruta_info.get("geo_epgs_4326_latlon").get("lat")
                longitud = ruta_info.get("geo_epgs_4326_latlon").get("lon")

                if latitud and longitud:
                    latlon_key = (float(latitud), float(longitud))
                    if latlon_key not in dades_punts:
                        dades_punts[latlon_key] = Punt(
                            latitud=latlon_key[0],
                            longitud=latlon_key[1],
                            altitud=0.0,
                            index_qualitat_aire=0.0
                        )

                if ruta_id and ruta_nombre and ruta_descripcio:
                    dades_rutes.append((ruta_id, ruta_nombre, ruta_descripcio, 0.0, latlon_key))

            with transaction.atomic():
                punts_creats = Punt.objects.bulk_create(
                    dades_punts.values(),
                    update_conflicts=True,
                    unique_fields=["latitud", "longitud"],
                    update_fields=["altitud", "index_qualitat_aire"]
                )

            punts_guardats = {(p.latitud, p.longitud): p.id for p in punts_creats}

            rutas_a_crear = [
                Ruta(
                    id=ruta_id,
                    nom=nombre,
                    descripcio=descripcion,
                    dist_km=dist_km,
                    punt_inici_id=punts_guardats.get(punt, None)
                )
                for ruta_id, nombre, descripcion, dist_km, punt in dades_rutes
            ]

            with transaction.atomic():
                Ruta.objects.bulk_create(rutas_a_crear, ignore_conflicts=True)

            job.last_run = now()
            with transaction.atomic():
                job.save()

def actualitzar_estacions_qualitat_aire():
    job, created = JobExecution.objects.get_or_create(name="actualitzar_estacions_qualitat_aire")
    if created or now() - job.last_run >= timedelta(days=1):

        response = requests.get(DADES_OBERTES_DE_LA_GENERALITAT_URL)
        if response.status_code == 200:
            dades = response.json()
            dades_punts = {}
            dades_estacions = []
            dades_contaminants = []
            dades_presencia = []

            for presencia_info in dades:
                data = presencia_info.get("data")
                valor = presencia_info.get("magnitud")
                nom_contaminant = presencia_info.get("contaminant")
                latitud = presencia_info.get("latitud")
                longitud = presencia_info.get("longitud")
                altitud = presencia_info.get("altitud")
                nom_estacio = presencia_info.get("nom_estacio")

                if nom_contaminant:
                    dades_contaminants.append(Contaminant(nom=nom_contaminant, informacio=""))

                if latitud and longitud:
                    latlon_key = (float(latitud), float(longitud))
                    if latlon_key not in dades_punts:
                        dades_punts[latlon_key] = Punt(
                            latitud=latlon_key[0],
                            longitud=latlon_key[1],
                            altitud=altitud if altitud else 0.0,
                            index_qualitat_aire=0.0
                        )
                
                if nom_estacio and latlon_key:
                    dades_estacions.append((nom_estacio, "", latlon_key))

                if data and valor and nom_contaminant and latlon_key:
                    dades_presencia.append((data, valor, nom_contaminant, latlon_key))

            with transaction.atomic():
                contaminants_creats = Contaminant.objects.bulk_create(dades_contaminants, ignore_conflicts=True)
            
            contaminants_guardats = {(c.nom): c.id for c in contaminants_creats}

            with transaction.atomic():
                punts_creats = Punt.objects.bulk_create(
                    list(dades_punts.values()),
                    update_conflicts=True,
                    unique_fields=["latitud", "longitud"],
                    update_fields=["altitud"]
                )

            punts_guardats = {(p.latitud, p.longitud): p for p in punts_creats}
            
            for nom_estacio, descripcio, latlon_key in dades_estacions:
                print(str(latlon_key))
                punt = punts_guardats.get(latlon_key)
                if punt:
                    print(str(punt.id))
                    print(str(punt))
                    print(Punt.objects.filter(id=punt.id).values())
                    print(EstacioQualitatAire.objects.filter(punt_ptr_id=punt.id).exists())
                    #print(EstacioQualitatAire.objects.filter(punt_ptr=punt).exists())
                    #print(EstacioQualitatAire.objects.filter(id=punt.id).exists())
                    print(Punt.objects.filter(id=punt.id).exists())
                    with transaction.atomic():
                        EstacioQualitatAire.objects.get_or_create(
                            #punt_ptr=punt,
                            punt_ptr_id=punt.id,
                            #id=punt.id,
                            defaults={"nom_estacio": nom_estacio, "descripcio": descripcio}
                        )

            presencies_a_crear = [
                Presencia(
                    data=data,
                    valor=valor,
                    contaminant_id=contaminants_guardats.get(contaminant, None),
                    punt_id=punts_guardats.get(latlon_key, None)                    
                )
                for data, valor, contaminant, latlon_key in dades_presencia
            ]

            with transaction.atomic():
                Presencia.objects.bulk_create(presencies_a_crear, ignore_conflicts=True)

            job.last_run = now()
            with transaction.atomic():
                job.save()

def actualitzar_activitats_culturals():
    job, created = JobExecution.objects.get_or_create(name=f"actualitzar_activitats_culturals")
    if created or now() - job.last_run >= timedelta(days=1):

        response = requests.get(SERVEI_ACTIVITATS_CULTURALS_URL)
        if response.status_code == 200:

            dades = response.json()
            with transaction.atomic():
                for activitat_dades in dades:
                    nom = activitat_dades.get("nom")
                    descripcio = activitat_dades.get("descripcio")
                    data_inici = activitat_dades.get("data_inici")
                    data_fi = activitat_dades.get("data_fi")
                    altitud = activitat_dades.get("altitud")
                    latitud = activitat_dades.get("latitud")
                    longitud = activitat_dades.get("longitud")

                    if latitud and longitud and altitud and nom and descripcio and data_inici:
                        activitat_info = {
                            "nom_activitat": nom,
                            "descripcio": descripcio,
                            "latitud": float(latitud),
                            "longitud": float(longitud),
                            "altitud": float(altitud),
                            "index_qualitat_aire": 0.0,
                            "data_inici": data_inici,
                            "data_fi": data_fi
                        }
                        activitat_serializer = ActivitatCulturalSerializer(data=activitat_info)
                        if activitat_serializer.is_valid() and not ActivitatCultural.objects.filter(nom_activitat=nom).exists():
                            activitat_serializer.save()
            
            job.last_run = now()
            job.save()