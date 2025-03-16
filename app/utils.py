import requests
from django.utils.timezone import now, timedelta
from .models import JobExecution, Presencia, Contaminant, Ruta, Punt, EstacioQualitatAire, ActivitatCultural
from django.db import transaction
from rest_framework.exceptions import ValidationError
from app.serializers import PresenciaSerializer, RutaSerializer, ContaminantSerializer, PuntSerializer, EstacioQualitatAireSerializer, ActivitatCulturalSerializer

OPEN_DATA_BCN_URL = "https://opendata-ajuntament.barcelona.cat/data/dataset/8f9f4b41-3260-4009-b6a2-80c9810776be/resource/d594937a-1ed0-4f08-8902-8bff2fcbd8b1/download"
DADES_OBERTES_DE_LA_GENERALITAT_URL = "https://analisi.transparenciacatalunya.cat/resource/tasf-thgu.json" #"?$select=nom_estacio,altitud,latitud,longitud,contaminant,data,magnitud"
SERVEI_ACTIVITATS_CULTURALS_URL = "https://???"

def actualitzar_rutes():
    job, created = JobExecution.objects.get_or_create(name="actualizar_rutas")
    
    if created or now() - job.last_run >= timedelta(weeks=1):
        response = requests.get(OPEN_DATA_BCN_URL)
        if response.status_code == 200:
            dades = response.json()

            with transaction.atomic():
                for ruta_info in dades:
                    ruta_id = ruta_info.get('register_id')
                    ruta_nombre = ruta_info.get('name')
                    ruta_descripcio = ruta_info.get('body')
                    latitud = ruta_info.get('geo_epgs_4326_lat')
                    longitud = ruta_info.get('geo_epgs_4326_lon')

                    if latitud and longitud:
                        punto_info = {
                            'latitud': float(latitud),
                            'longitud': float(longitud),
                            'altitud': 0.0,
                            'index_qualitat_aire': 0.0
                        }
                        punto_serializer = PuntSerializer(data=punto_info)
                        if punto_serializer.is_valid() and not Punt.objects.filter(latitud=float(latitud), longitud=float(longitud)).exists():
                            punto = punto_serializer.save()

                    if ruta_id and ruta_nombre and ruta_descripcio and punto:
                        ruta_info = {
                            'id': ruta_id,
                            'nom': ruta_nombre,
                            'descripcio': ruta_descripcio,
                            'dist_km': 0.0,
                            'punts': [punto.id]
                        }
                        ruta_serializer = RutaSerializer(data=ruta_info)
                        if ruta_serializer.is_valid() and not Ruta.objects.filter(id=ruta_id).exists():
                            ruta_serializer.save()
            
            job.last_run = now()
            job.save()

def actualitzar_estacions_qualitat_aire():
    job, created = JobExecution.objects.get_or_create(name="actualitzar_estacions_qualitat_aire")

    if created or now() - job.last_run >= timedelta(days=1):
        response = requests.get(DADES_OBERTES_DE_LA_GENERALITAT_URL)
        if response.status_code == 200:
            dades = response.json()
            
            with transaction.atomic():
                for presencia_dades in dades:
                    nom_estacio = presencia_dades.get('nom_estacio')
                    altitud = presencia_dades.get('altitud')
                    latitud = presencia_dades.get('latitud')
                    longitud = presencia_dades.get('longitud')
                    contaminant = presencia_dades.get('contaminant')
                    data = presencia_dades.get('data')
                    valor = presencia_dades.get('magnitud')

                    if altitud and latitud and longitud and nom_estacio:
                        estacio_info = {
                            'nom': nom_estacio,
                            'descripcio': '',
                            'latitud': float(latitud),
                            'longitud': float(longitud),
                            'altitud': float(altitud),
                            'index_qualitat_aire': 0.0
                        }
                        estacio_serializer =EstacioQualitatAireSerializer(data=estacio_info)
                        if estacio_serializer.is_valid() and not EstacioQualitatAire.objects.filter(nom=nom_estacio).exists():
                            estacio = estacio_serializer.save()
                    
                    if contaminant:
                        contaminant_info = {
                            'nom': contaminant,
                            'informacio': ''
                        }
                        contaminant_serializer = ContaminantSerializer(data=contaminant_info)
                        if contaminant_serializer.is_valid() and not Contaminant.objects.filter(nom=contaminant).exists():
                            contaminant = contaminant_serializer.save()

                    if estacio and contaminant and data:
                        presencia_info = {
                            'punt': estacio.id,
                            'contaminant': contaminant.id,
                            'data': data,
                            'valor': valor
                        }
                        presencia_serializer = PresenciaSerializer(data=presencia_info)
                        if presencia_serializer.is_valid():
                            presencia_serializer.save()
            
            job.last_run = now()
            job.save()

def actualitzar_activitats_culturals():
    job, created = JobExecution.objects.get_or_create(name=f"actualitzar_activitats_culturals")

    if created or now() - job.last_run >= timedelta(days=1):
        response = requests.get(SERVEI_ACTIVITATS_CULTURALS_URL)
        if response.status_code == 200:
            dades = response.json()
            
            with transaction.atomic():
                for activitat_dades in dades:
                    nom = activitat_dades.get('nom')
                    descripcio = activitat_dades.get('descripcio')
                    data_inici = activitat_dades.get('data_inici')
                    data_fi = activitat_dades.get('data_fi')
                    altitud = activitat_dades.get('altitud')
                    latitud = activitat_dades.get('latitud')
                    longitud = activitat_dades.get('longitud')

                    if latitud and longitud and altitud and nom and descripcio and data_inici:
                        activitat_info = {
                            'nom_activitat': nom,
                            'descripcio': descripcio,
                            'latitud': float(latitud),
                            'longitud': float(longitud),
                            'altitud': float(altitud),
                            'index_qualitat_aire': 0.0,
                            'data_inici': data_inici,
                            'data_fi': data_fi
                        }
                        activitat_serializer = ActivitatCulturalSerializer(data=activitat_info)
                        if activitat_serializer.is_valid() and not ActivitatCultural.objects.filter(nom_activitat=nom).exists():
                            activitat_serializer.save()
                        else:
                            continue  # O manejar el error según sea necesario
            
            job.last_run = now()
            job.save()