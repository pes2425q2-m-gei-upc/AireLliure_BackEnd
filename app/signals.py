import datetime
import os
import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import (
    ActivitatCultural,
    Amistat,
    Apuntat,
    Bloqueig,
    Contaminant,
    EstacioQualitatAire,
    EventDeCalendari,
    EventDeCalendariPrivat,
    EventDeCalendariPublic,
    Missatge,
    Punt,
    Recompensa,
    Usuari,
    Valoracio,
    Xat,
    XatGrupal,
    XatIndividual,
    Invitacio,
    JobExecution,
    IndexQualitatAire,
    DificultatEsportiva,
    AccesibilitatRespiratoria,
    AssignaDificultatEsportiva,
    AssignaAccesibilitatRespiratoria,
    Admin,
)


def notificar_cambio_modelo(sender, instance, created=None, **kwargs):
    try:
        # Si estamos corriendo tests, no hacer nada
        if os.environ.get("DISABLE_SIGNALS", "").lower() == "true":
            return

        # Determinar el tipo de operación
        if created is None:  # Es una operación de eliminación
            evento = "eliminado"
        elif created:  # Es una operación de creación
            evento = "creado"
        else:  # Es una operación de actualización
            # Verificar si es un PATCH (actualización parcial)
            if hasattr(instance, '_changed_fields'):
                evento = "patch"
            else:
                evento = "modificado"

        # Serializar los datos del modelo
        datos_modelo = serializers.serialize("json", [instance])
        datos_dict = next(serializers.deserialize("json", datos_modelo)).object.__dict__

        # Eliminar campos internos de Django que no necesitamos
        campos_a_eliminar = ["_state", "password"]
        for campo in campos_a_eliminar:
            datos_dict.pop(campo, None)

        # Convierte todos los valores datetime en datos_dict a string ISO
        for k, v in datos_dict.items():
            if isinstance(v, datetime.datetime):
                datos_dict[k] = v.isoformat()
            elif isinstance(v, datetime.date):
                datos_dict[k] = v.isoformat()

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
        if isinstance(timestamp, datetime.datetime):
            timestamp = timestamp.isoformat()
        elif isinstance(timestamp, datetime.date):
            timestamp = timestamp.isoformat()

        # Logging detallado
        logging.info(
            f"SEÑAL DISPARADA: {sender.__name__} - {obj_id} - {evento} - "
            f"Timestamp: {timestamp}"
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
                    "campos_modificados": getattr(instance, '_changed_fields', None),
                },
            },
        )

    except Exception as e:
        logging.error(f"Error en notificar_cambio_modelo: {str(e)}")
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
    JobExecution,
    IndexQualitatAire,
    DificultatEsportiva,
    AccesibilitatRespiratoria,
]

for modelo in modelos:
    receiver(post_save, sender=modelo)(notificar_cambio_modelo)
    receiver(post_delete, sender=modelo)(notificar_cambio_modelo)
