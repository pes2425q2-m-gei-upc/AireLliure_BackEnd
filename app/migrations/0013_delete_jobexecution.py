# Generated by Django 5.1.5 on 2025-05-05 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0012_alter_ruta_imatge_alter_usuari_imatge"),
    ]

    operations = [
        migrations.DeleteModel(
            name="JobExecution",
        ),
    ]
