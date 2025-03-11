import requests
from django.utils.timezone import now, timedelta
from .models import JobExecution, Ruta, EstacioQualitatAire, ActivitatCultural

OPEN_DATA_BCN_URL = "https://opendata-ajuntament.barcelona.cat/data/api/action/package_show?id=np-circuits-caminar-correr"
# DADES_OBERTES_DE_LA_GENERALITAT_URL = "https://https://gestorapi.gencat.cat/dadesobertes/consulta/consultadades/???"
DADES_OBERTES_DE_LA_GENERALITAT_URL = "https://analisi.transparenciacatalunya.cat/resource/tasf-thgu.json"
SERVEI_ACTIVITATS_CULTURALS_URL = "https://???"

def actualitzar_rutes():
    job, created = JobExecution.objects.get_or_create(name="actualitzar_rutes")

    if now() - job.last_run >= timedelta(days=1):
        response = requests.get(OPEN_DATA_BCN_URL)
        if response.status_code == 200:
            datos = response.json()

            # Borra los datos actuales
            Ruta.objects.all().delete()

            # Guarda los nuevos datos
            objetos = [Ruta(**dato) for dato in datos]
            Ruta.objects.bulk_create(objetos)

            # Actualiza el tiempo de última ejecución
            job.last_run = now()
            job.save()

def actualitzar_estacions_qualitat_aire():
    job, created = JobExecution.objects.get_or_create(name="actualitzar_estacions_qualitat_aire")

    if now() - job.last_run >= timedelta(days=1):
        response = requests.get(DADES_OBERTES_DE_LA_GENERALITAT_URL)
        if response.status_code == 200:
            datos = response.json()

            # Borra los datos actuales
            EstacioQualitatAire.objects.all().delete()

            # Guarda los nuevos datos
            objetos = [EstacioQualitatAire(**dato) for dato in datos]
            EstacioQualitatAire.objects.bulk_create(objetos)

            # Actualiza el tiempo de última ejecución
            job.last_run = now()
            job.save()

def actualitzar_activitats_culturals():
    job, created = JobExecution.objects.get_or_create(name="actualitzar_activitats_culturals")

    if now() - job.last_run >= timedelta(days=1):
        response = requests.get(SERVEI_ACTIVITATS_CULTURALS_API)
        if response.status_code == 200:
            datos = response.json()

            # Borra los datos actuales
            ActivitatCultural.objects.all().delete()

            # Guarda los nuevos datos
            objetos = [ActivitatCultural(**dato) for dato in datos]
            ActivitatCultural.objects.bulk_create(objetos)

            # Actualiza el tiempo de última ejecución
            job.last_run = now()
            job.save()