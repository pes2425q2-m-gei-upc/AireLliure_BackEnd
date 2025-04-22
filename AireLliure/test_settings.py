from .settings import *

# Desactivar todos los middlewares durante las pruebas
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Usar una base de datos en memoria para pruebas
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Desactivar la validación de contraseñas durante las pruebas
AUTH_PASSWORD_VALIDATORS = []

# Desactivar la actualización automática de datos durante las pruebas
DISABLE_AUTO_UPDATE = True
