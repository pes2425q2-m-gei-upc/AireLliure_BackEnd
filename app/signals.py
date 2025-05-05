import datetime
import logging
import os

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import (
    AccesibilitatRespiratoria,
    ActivitatCultural,
    Admin,
    Amistat,
    Apuntat,
    AssignaAccesibilitatRespiratoria,
    AssignaDificultatEsportiva,
    Bloqueig,
    Contaminant,
    DificultatEsportiva,
    EstacioQualitatAire,
    EventDeCalendari,
    EventDeCalendariPrivat,
    EventDeCalendariPublic,
    IndexQualitatAire,
    Invitacio,
    Missatge,
    Punt,
    Recompensa,
    Usuari,
    Valoracio,
    Xat,
    XatGrupal,
    XatIndividual,
)


def _get_event_type(created, instance):
    """Determina el tipo de evento basado en el parámetro created y el estado de la instancia."""  # noqa: B950
    if created is None:
        return "eliminado"
    if created:
        return "creado"
    return "patch" if hasattr(instance, "_changed_fields") else "modificado"


def _process_datetime_values(datos_dict):
    """Procesa los valores datetime en el diccionario."""
    for k, v in datos_dict.items():
        if isinstance(v, (datetime.datetime, datetime.date)):
            datos_dict[k] = v.isoformat()


def notificar_cambio_modelo(sender, instance, created=None, **kwargs):
    """Notifica cambios en los modelos a través de WebSocket."""
    try:
        # Si estamos corriendo tests, no hacer nada
        if os.environ.get("DISABLE_SIGNALS", "").lower() == "true":
            return

        evento = _get_event_type(created, instance)

        # Serializar los datos del modelo
        datos_modelo = serializers.serialize("json", [instance])
        datos_dict = next(serializers.deserialize("json", datos_modelo)).object.__dict__

        # Eliminar campos internos de Django que no necesitamos
        campos_a_eliminar = ["_state", "password"]
        for campo in campos_a_eliminar:
            datos_dict.pop(campo, None)

        # Procesar valores datetime
        _process_datetime_values(datos_dict)

        # Determinar el identificador primario del objeto
        obj_id = None
        for field in instance._meta.fields:
            if field.primary_key:
                obj_id = getattr(instance, field.name)
                break

        # Convierte timestamp si es datetime
        timestamp = (
            instance._meta.get_field("data").value_from_object(instance)
            if hasattr(instance, "data")
            else datetime.datetime.now()
        )
        if isinstance(timestamp, (datetime.datetime, datetime.date)):
            timestamp = timestamp.isoformat()

        # Logging detallado
        logging.info(
            "SEÑAL DISPARADA: %s - %s - %s - Timestamp: %s",
            sender.__name__,
            obj_id,
            evento,
            timestamp,
        )

        # Enviar notificación a través del canal WebSocket
        async_to_sync(get_channel_layer().group_send)(
            "model_updates",
            {
                "type": "send_model_update",
                "data": {
                    "tipo": evento,
                    "modelo": sender.__name__,
                    "id": obj_id,
                    "datos": datos_dict,
                    "timestamp": timestamp,
                    "operacion": evento.upper(),
                    "campos_modificados": getattr(instance, "_changed_fields", None),
                },
            },
        )

    except (serializers.base.DeserializationError, AttributeError, ValueError) as e:
        logging.error("Error en notificar_cambio_modelo: %s", str(e))
        # No propagamos la excepción para no interrumpir el flujo normal


# Registrar señales para todos los modelos
modelos = [
    # Modelos de la app
    Usuari,
    Admin,
    Bloqueig,
    Amistat,
    Valoracio,
    Recompensa,
    AssignaDificultatEsportiva,
    AssignaAccesibilitatRespiratoria,
    Xat,
    XatIndividual,
    XatGrupal,
    Invitacio,
    Missatge,
    EventDeCalendari,
    EventDeCalendariPrivat,
    EventDeCalendariPublic,
    Apuntat,
    Punt,
    EstacioQualitatAire,
    ActivitatCultural,
    Contaminant,
    IndexQualitatAire,
    DificultatEsportiva,
    AccesibilitatRespiratoria,
]

for modelo in modelos:
    receiver(post_save, sender=modelo)(notificar_cambio_modelo)
    receiver(post_delete, sender=modelo)(notificar_cambio_modelo)
