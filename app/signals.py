from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import (
    ActivitatCultural,
    Apuntat,
    Contaminant,
    EstacioQualitatAire,
    EventDeCalendari,
    EventDeCalendariPrivat,
    EventDeCalendariPublic,
    Missatge,
    Presencia,
    Punt,
    Recompensa,
    Ruta,
    Usuari,
    Valoracio,
    Xat,
    XatGrupal,
)


def notificar_cambio_modelo(sender, instance, created=None, **kwargs):
    evento = (
        "creado" if created else "modificado" if created is not None else "eliminado"
    )

    # Serializar los datos del modelo
    datos_modelo = serializers.serialize("json", [instance])
    datos_dict = (
        serializers.deserialize("json", datos_modelo)
        .__next__()
        .object.__dict__  # pylint: disable=unnecessary-dunder-call
    )

    # Eliminar campos internos de Django que no necesitamos
    campos_a_eliminar = ["_state", "password"]
    for campo in campos_a_eliminar:
        datos_dict.pop(campo, None)

    # Determinar el identificador primario del objeto
    if hasattr(instance, "id"):
        obj_id = instance.id
    elif hasattr(instance, "pk"):
        obj_id = instance.pk
    elif hasattr(instance, "correu"):
        obj_id = instance.correu
    else:
        # Busca el primer campo que sea primary_key
        obj_id = None
        for field in instance._meta.fields:
            if field.primary_key:
                obj_id = getattr(instance, field.name)
                break

    print(f"SEÑAL DISPARADA: {sender.__name__} - {obj_id} - created={created}")

    async_to_sync(get_channel_layer().group_send)(
        "model_updates",
        {
            "type": "send_model_update",
            "data": {
                "tipo": evento,
                "modelo": sender.__name__,
                "id": obj_id,
                "datos": datos_dict,
                "timestamp": (
                    instance._meta.get_field("data").value_from_object(instance)
                    if hasattr(instance, "data")
                    else None
                ),
            },
        },
    )


# Registrar señales para todos los modelos

modelos = [
    # Modelos de la app
    Usuari,
    Ruta,
    Valoracio,
    Recompensa,
    Xat,
    XatGrupal,
    Missatge,
    EventDeCalendari,
    EventDeCalendariPrivat,
    EventDeCalendariPublic,
    Apuntat,
    Punt,
    EstacioQualitatAire,
    ActivitatCultural,
    Contaminant,
    Presencia,
]

for modelo in modelos:
    receiver(post_save, sender=modelo)(notificar_cambio_modelo)
    receiver(post_delete, sender=modelo)(notificar_cambio_modelo)
