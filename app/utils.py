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

    if created: print("job actualizar_rutas created")
    else:       print("job actualizar_rutas retrieved")
    
    if created or now() - job.last_run >= timedelta(weeks=1):
        response = requests.get(OPEN_DATA_BCN_URL)
        
        print(OPEN_DATA_BCN_URL + " response: " + response.status_code)

        if response.status_code == 200:
            dades = response.json()

            print("conversió json: " + dades)

            with transaction.atomic():
                for ruta_info in dades:

                    ruta_id = ruta_info.get('register_id')
                    print(ruta_id)

                    ruta_nombre = ruta_info.get('name')
                    print(ruta_nombre)

                    ruta_descripcio = ruta_info.get('body')
                    print(ruta_descripcio)

                    latitud = ruta_info.get('geo_epgs_4326_lat')
                    print(latitud)

                    longitud = ruta_info.get('geo_epgs_4326_lon')
                    print(longitud)

                    if latitud and longitud:
                        punto_info = {
                            'latitud': float(latitud),
                            'longitud': float(longitud),
                            'altitud': 0.0,
                            'index_qualitat_aire': 0.0
                        }

                        print("punto info: " + punto_info)
                        
                        punto_serializer = PuntSerializer(data=punto_info)

                        print("punto_serializer: " + punto_serializer.data)
                        
                        if punto_serializer.is_valid():
                            print("punto_serializer is valid")

                            if not Punt.objects.filter(latitud=float(latitud), longitud=float(longitud)).exists():
                                print("punto no existe")
                                punto = punto_serializer.save()
                                print("punto guardado")

                    if ruta_id and ruta_nombre and ruta_descripcio and punto:
                        ruta_info = {
                            'id': ruta_id,
                            'nom': ruta_nombre,
                            'descripcio': ruta_descripcio,
                            'dist_km': 0.0,
                            'punts': [punto.id]
                        }

                        print("ruta info: " + ruta_info)

                        ruta_serializer = RutaSerializer(data=ruta_info)

                        print("ruta_serializer: " + ruta_serializer.data)
                        
                        if ruta_serializer.is_valid():
                            print("ruta_serializer is valid")
                            if not Ruta.objects.filter(id=ruta_id).exists():
                                print("ruta no existe")
                                ruta_serializer.save()
                                print("ruta guardada")
            
            job.last_run = now()
            job.save()
            print("job actualizar_rutas updated")

def actualitzar_estacions_qualitat_aire():
    job, created = JobExecution.objects.get_or_create(name="actualitzar_estacions_qualitat_aire")

    if created: print("job actualitzar_estacions_qualitat_aire created")
    else:       print("job actualitzar_estacions_qualitat_aire retrieved")

    if created or now() - job.last_run >= timedelta(days=1):
        response = requests.get(DADES_OBERTES_DE_LA_GENERALITAT_URL)

        print(DADES_OBERTES_DE_LA_GENERALITAT_URL + " response: " + response.status_code)

        if response.status_code == 200:
            dades = response.json()
            
            print("conversió json: " + dades)
            
            with transaction.atomic():
                for presencia_dades in dades:
                    nom_estacio = presencia_dades.get('nom_estacio')
                    print(nom_estacio)

                    altitud = presencia_dades.get('altitud')
                    print(altitud)

                    latitud = presencia_dades.get('latitud')
                    print(latitud)
                    
                    longitud = presencia_dades.get('longitud')
                    print(longitud)
                    
                    contaminant = presencia_dades.get('contaminant')
                    print(contaminant)
                    
                    data = presencia_dades.get('data')
                    print(data)
                    
                    valor = presencia_dades.get('magnitud')
                    print(valor)
                    
                    if altitud and latitud and longitud and nom_estacio:
                        estacio_info = {
                            'nom': nom_estacio,
                            'descripcio': '',
                            'latitud': float(latitud),
                            'longitud': float(longitud),
                            'altitud': float(altitud),
                            'index_qualitat_aire': 0.0
                        }

                        print("estacio info: " + estacio_info)
                        
                        estacio_serializer =EstacioQualitatAireSerializer(data=estacio_info)

                        print("estacio_serializer: " + estacio_serializer.data)

                        if estacio_serializer.is_valid():
                            print("estacio_serializer is valid")
                            if not EstacioQualitatAire.objects.filter(nom=nom_estacio).exists():
                                print("estacio no existe")
                                estacio = estacio_serializer.save()
                                print("estacio guardada")
                    
                    if contaminant:
                        contaminant_info = {
                            'nom': contaminant,
                            'informacio': ''
                        }
                        
                        print("contaminant_info: " + contaminant_info)

                        contaminant_serializer = ContaminantSerializer(data=contaminant_info)

                        print("contaminant_serializer: " + contaminant_serializer.data)
                        
                        if contaminant_serializer.is_valid():
                            print("contaminant_serializer is valid")
                            if not Contaminant.objects.filter(nom=contaminant).exists():
                                print("contaminant no existe")
                                contaminant = contaminant_serializer.save()
                                print("contaminant guardada")

                    if estacio and contaminant and data:
                        presencia_info = {
                            'punt': estacio.id,
                            'contaminant': contaminant.id,
                            'data': data,
                            'valor': valor
                        }

                        print("presencia_info: " + presencia_info)

                        presencia_serializer = PresenciaSerializer(data=presencia_info)

                        print("presencia_serializer: " + presencia_serializer.data)

                        if presencia_serializer.is_valid():
                            print("presencia_serializer is valid")
                            presencia_serializer.save()
                            print("presencia guardada")
            
            job.last_run = now()
            job.save()
            print("job actualitzar_estacions_qualitat_aire updated")


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