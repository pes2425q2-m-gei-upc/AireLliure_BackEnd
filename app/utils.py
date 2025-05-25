# pylint: disable=too-many-locals, too-many-nested-blocks, too-many-statements

from datetime import datetime, time

import requests
from django.db import transaction
from django.utils.timezone import make_aware, now, timedelta

from .models import (
    ActivitatCultural,
    Contaminant,
    EstacioQualitatAire,
    IndexQualitatAire,
    Presencia,
    Punt,
    Ruta,
)

OPEN_DATA_BCN_URL = (
    "https://opendata-ajuntament.barcelona.cat/"
    "data/dataset/8f9f4b41-3260-4009-b6a2-80c9810776be/"
    "resource/d594937a-1ed0-4f08-8902-8bff2fcbd8b1/download"
)
DADES_OBERTES_DE_LA_GENERALITAT_URL = (
    "https://analisi.transparenciacatalunya.cat/resource/tasf-thgu.json"
    # "?$select=nom_estacio,altitud,latitud,longitud,contaminant,data,magnitud"
)
SERVEI_ACTIVITATS_CULTURALS_URL = "http://nattech.fib.upc.edu:40340/service/events-all"


def genera_ruta_id(register_id) -> int:
    return register_id % (2**31)


def datetime_from_iso_date_and_hour(iso_date_str: str, hora: int) -> datetime:
    fecha_base = datetime.fromisoformat(iso_date_str).date()
    result = fecha_base
    if hora == 24:
        result = datetime.combine(fecha_base + timedelta(days=1), time(0))
    else:
        result = datetime.combine(fecha_base, time(hora))
    return make_aware(result)


def actualitzar_rutes():
    response = requests.get(OPEN_DATA_BCN_URL, timeout=60)
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
                        index_qualitat_aire=0.0,
                    )

                if ruta_id and ruta_nombre and ruta_descripcio:
                    dades_rutes.append(
                        (ruta_id, ruta_nombre, ruta_descripcio, 0.0, latlon_key)
                    )

        with transaction.atomic():
            Punt.objects.bulk_create(
                list(dades_punts.values()),
                ignore_conflicts=True,
                unique_fields=["latitud", "longitud"],
            )

        with transaction.atomic():
            punts_guardats = {
                (p.latitud, p.longitud): p.id
                for p in Punt.objects.filter(
                    latitud__in=[k[0] for k in dades_punts],
                    longitud__in=[k[1] for k in dades_punts],
                )
            }

        rutas_a_crear = [
            Ruta(
                id=ruta_id,
                nom=nombre,
                descripcio=descripcion,
                dist_km=dist_km,
                punt_inici_id=punts_guardats.get(punt),
            )
            for ruta_id, nombre, descripcion, dist_km, punt in dades_rutes
        ]

        with transaction.atomic():
            Ruta.objects.bulk_create(rutas_a_crear, ignore_conflicts=True)


def actualitzar_estacions_qualitat_aire():
    response = requests.get(DADES_OBERTES_DE_LA_GENERALITAT_URL, timeout=60)
    if response.status_code == 200:
        dades = response.json()
        dades_punts = {}
        dades_estacions = {}
        dades_contaminants = {}
        dades_presencia = []

        for presencia_info in dades:
            data = presencia_info.get("data")
            nom_contaminant = presencia_info.get("contaminant")
            latitud = presencia_info.get("latitud")
            longitud = presencia_info.get("longitud")
            nom_estacio = presencia_info.get("nom_estacio")

            if nom_contaminant:

                if nom_contaminant not in dades_contaminants:
                    dades_contaminants[nom_contaminant] = Contaminant(
                        nom=nom_contaminant, informacio=""
                    )

                if latitud and longitud:

                    latlon_key = (float(latitud), float(longitud))
                    if latlon_key not in dades_punts:

                        dades_punts[latlon_key] = Punt(
                            latitud=latlon_key[0],
                            longitud=latlon_key[1],
                            index_qualitat_aire=0.0,
                        )

                    if nom_estacio and nom_estacio not in dades_estacions:
                        dades_estacions[latlon_key] = EstacioQualitatAire(
                            nom_estacio=nom_estacio,
                            descripcio="",
                        )

                    if data:
                        dades_presencia.extend(
                            (
                                datetime_from_iso_date_and_hour(data, h),
                                float(valor),
                                nom_contaminant,
                                latlon_key,
                            )
                            for h in range(1, 25)
                            if (valor := presencia_info.get(f"h{h:02}")) is not None
                        )

        with transaction.atomic():
            Contaminant.objects.bulk_create(
                list(dades_contaminants.values()), ignore_conflicts=True
            )

        with transaction.atomic():
            contaminants_guardats = {
                c.nom: c
                for c in Contaminant.objects.filter(
                    nom__in=list(dades_contaminants.keys())
                )
            }

        with transaction.atomic():
            indexos_qualitat_aire_guardats = {
                index.contaminant.nom: index
                for index in IndexQualitatAire.objects.select_related(
                    "contaminant"
                ).all()
            }

        with transaction.atomic():
            Punt.objects.bulk_create(
                list(dades_punts.values()),
                ignore_conflicts=True,
                unique_fields=["latitud", "longitud"],
            )

        with transaction.atomic():
            punts_guardats = {
                (p.latitud, p.longitud): p.id
                for p in Punt.objects.filter(
                    latitud__in=[k[0] for k in dades_punts],
                    longitud__in=[k[1] for k in dades_punts],
                )
            }

        for latlon_key, estacio in dades_estacions.items():
            punt_id = punts_guardats.get(latlon_key)
            nom_estacio = estacio.nom_estacio
            descripcio = estacio.descripcio

            with transaction.atomic():
                EstacioQualitatAire.objects.get_or_create(
                    punt_ptr_id=punt_id,
                    defaults={
                        "nom_estacio": nom_estacio,
                        "descripcio": descripcio,
                        "latitud": latlon_key[0],
                        "longitud": latlon_key[1],
                        "index_qualitat_aire": 0.0,
                    },
                )

        presencies_a_crear = [
            Presencia(
                data=data,
                valor=valor,
                valor_iqa=(
                    indexos_qualitat_aire_guardats.get(
                        nom_contaminant
                    ).normalitzar_valor(valor)
                    if indexos_qualitat_aire_guardats.get(nom_contaminant) is not None
                    else 0.0
                ),
                contaminant_id=contaminants_guardats.get(nom_contaminant).id,
                punt_id=punts_guardats.get(latlon_key),
            )
            for data, valor, nom_contaminant, latlon_key in dades_presencia
        ]

        with transaction.atomic():
            Presencia.objects.bulk_create(presencies_a_crear, ignore_conflicts=True)

        ahir = now().date() - timedelta(days=1)
        with transaction.atomic():
            Presencia.objects.filter(data__date__lt=ahir).delete()


def actualitzar_activitats_culturals():

    response = requests.get(SERVEI_ACTIVITATS_CULTURALS_URL, timeout=60)
    if response.status_code == 200:
        dades = response.json().get("events")
        dades_punts = {}
        punts_guardats = {}
        dades_activitats = []

        for activitat_dades in dades:
            nom = activitat_dades.get("name")
            descripcio = activitat_dades.get("description")
            data_inici = activitat_dades.get("start date")
            data_fi = activitat_dades.get("end date")
            latitud = activitat_dades.get("addressid").get("latitude")
            longitud = activitat_dades.get("addressid").get("longitude")

            if latitud and longitud:

                latlon_key = (float(latitud), float(longitud))
                if latlon_key not in dades_punts:

                    dades_punts[latlon_key] = Punt(
                        latitud=latlon_key[0],
                        longitud=latlon_key[1],
                        index_qualitat_aire=0.0,
                    )

                if nom and descripcio and data_inici:
                    data_inici = datetime.fromisoformat(data_inici).date()
                    data_fi = datetime.fromisoformat(data_fi).date()
                    dades_activitats.append(
                        (nom, descripcio, data_inici, data_fi, latlon_key)
                    )

        with transaction.atomic():
            Punt.objects.bulk_create(
                list(dades_punts.values()),
                ignore_conflicts=True,
                unique_fields=["latitud", "longitud"],
            )

        with transaction.atomic():
            punts_guardats = {
                (p.latitud, p.longitud): p.id
                for p in Punt.objects.filter(
                    latitud__in=[k[0] for k in dades_punts],
                    longitud__in=[k[1] for k in dades_punts],
                )
            }

        avui = now().date()

        for nom, descripcio, data_inici, data_fi, latlon_key in dades_activitats:
            if data_fi >= avui:
                punt_id = punts_guardats.get(latlon_key)

                with transaction.atomic():
                    ActivitatCultural.objects.get_or_create(
                        punt_ptr_id=punt_id,
                        defaults={
                            "nom_activitat": nom,
                            "descripcio": descripcio[:255],
                            "data_inici": data_inici,
                            "data_fi": data_fi,
                            "latitud": latlon_key[0],
                            "longitud": latlon_key[1],
                            "index_qualitat_aire": 0.0,
                        },
                    )

        with transaction.atomic():
            activitats_a_eliminar = ActivitatCultural.objects.filter(data_fi__lt=avui)

        with transaction.atomic():
            punts_a_eliminar = (
                Punt.objects.filter(id__in=activitats_a_eliminar.values("id"))
                .exclude(id__in=EstacioQualitatAire.objects.values("id"))
                .exclude(id__in=Ruta.objects.values("punt_inici_id"))
            )

        with transaction.atomic():
            activitats_a_eliminar.delete()

        with transaction.atomic():
            punts_a_eliminar.delete()
