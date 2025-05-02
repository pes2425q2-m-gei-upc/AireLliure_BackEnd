# debug_s3.py

import os
import django

# 👉 Afegeix això abans de qualsevol import de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aire_lliure.settings")
django.setup()

from storages.backends.s3boto3 import S3Boto3Storage

try:
    storage = S3Boto3Storage()
    print("✅ S3Boto3Storage carregat:", storage.__class__)
    print("📂 Prova de llistat d'arxius al bucket:")
    print(storage.listdir(""))
except Exception as e:
    print("❌ ERROR connectant amb S3:")
    print(repr(e))
