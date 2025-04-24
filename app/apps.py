# pylint: disable=function-redefined

from django.apps import AppConfig


# REVISAR: 
# class AireLliureConfig(AppConfig):
class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
