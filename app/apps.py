# pylint: disable=function-redefined

from django.apps import AppConfig


# REVISAR:
# class AireLliureConfig(AppConfig):
class AireLliureAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        print("SEÑALES CARGADAS")
        import app.signals  # pylint: disable=import-outside-toplevel, unused-import
