import requests
from django.utils.timezone import now, timedelta
from .models import JobExecution, Ruta, EstacioQualitatAire, ActivitatCultural

OPEN_DATA_BCN_URL = "https://opendata-ajuntament.barcelona.cat/data/api/action/package_show?id=np-circuits-caminar-correr"
# DADES_OBERTES_DE_LA_GENERALITAT_URL = "https://https://gestorapi.gencat.cat/dadesobertes/consulta/consultadades/???"
DADES_OBERTES_DE_LA_GENERALITAT_URL = "https://analisi.transparenciacatalunya.cat/resource/tasf-thgu.json"
SERVEI_ACTIVITATS_CULTURALS_URL = "https://???"

def actualizar_datos(model, url, unique_field, interval):
    job, created = JobExecution.objects.get_or_create(name=f"actualizar_{model._meta.model_name}")

    if now() - job.last_run >= interval:
        response = requests.get(url)
        if response.status_code == 200:
            nuevos_datos = response.json()
            existentes = {getattr(obj, unique_field): obj for obj in model.objects.all()}
            nuevos = {dato[unique_field]: dato for dato in nuevos_datos}

            # Identificar objetos a eliminar
            ids_a_eliminar = set(existentes.keys()) - set(nuevos.keys())
            model.objects.filter(**{f"{unique_field}__in": ids_a_eliminar}).delete()

            # Identificar objetos a crear o actualizar
            objetos_a_guardar = []
            for dato in nuevos_datos:
                obj, created = model.objects.update_or_create(
                    **{unique_field: dato[unique_field]}, defaults=dato
                )
                objetos_a_guardar.append(obj)

            model.objects.bulk_update(objetos_a_guardar, nuevos_datos[0].keys())
            
            job.last_run = now()
            job.save()

def actualitzar_rutes():
    actualizar_datos(Ruta, OPEN_DATA_BCN_URL, "id", timedelta(weeks=1))

def actualitzar_estacions_qualitat_aire():
    actualizar_datos(EstacioQualitatAire, DADES_OBERTES_DE_LA_GENERALITAT_URL, "codi", timedelta(days=1))

def actualitzar_activitats_culturals():
    actualizar_datos(ActivitatCultural, SERVEI_ACTIVITATS_CULTURALS_URL, "id", timedelta(days=1))