# Generated by Django 5.1.5 on 2025-05-02 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0010_usuari_administrador"),
    ]

    operations = [
        migrations.AddField(
            model_name="ruta",
            name="imatge",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
        migrations.AddField(
            model_name="usuari",
            name="imatge",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]
