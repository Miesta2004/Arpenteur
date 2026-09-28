"""
Settings Django pour Arpenteur.
Voir dossier de conception, Partie 5 (cahier des charges technique) et Partie 8 (sécurité).
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent

# Charge backend/.env dans les variables d'environnement du process.
# Sans ça, os.environ.get(...) plus bas ne voit jamais ce que contient .env —
# c'était un manque avant (python-decouple était dans requirements.txt mais
# jamais utilisé). load_dotenv() ne fait rien si .env n'existe pas (silencieux).
load_dotenv(BASE_DIR / '.env')

# --- Sécurité : secrets en variables d'environnement, jamais en dur (Partie 8) ---
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-only-insecure-key-change-in-.env')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# GDAL/GEOS ne sont pas toujours trouvés automatiquement par Django selon l'OS/la
# version installée (fréquent sur Mac/Homebrew) — il faut alors préciser le chemin
# exact via ces deux variables. Ignoré si non défini (ex. sous Docker, où le
# Dockerfile installe GDAL à un emplacement standard, trouvé sans configuration).
GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH') or None
GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH') or None

# HTTPS obligatoire en production (Partie 8) — activé seulement quand DEBUG=False
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',  # PostGIS (Partie 5)

    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',

    'comptes',
    'activites',
    'organisations',
    'cartographie',
    'inventaire',
    'missions',
    'questionnaires',
    'rapports',
    'exportation',
    'notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'  # pour Django Channels (Partie 5)

# --- Base de données : PostgreSQL + PostGIS (Partie 5) ---
# Fonctionne aussi bien avec une instance locale qu'un Postgres managé distant
# (ex. Supabase) — seules les variables d'environnement changent, pas ce bloc.

DATABASES = {
    "default": dj_database_url.config(
        default=(
            f"postgis://{os.environ.get('POSTGRES_USER')}:"
            f"{os.environ.get('POSTGRES_PASSWORD')}@"
            f"{os.environ.get('POSTGRES_HOST')}:"
            f"{os.environ.get('POSTGRES_PORT', '5432')}/"
            f"{os.environ.get('POSTGRES_DB')}"
        ),
        conn_max_age=600,
        ssl_require=True,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Dakar'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Django REST Framework ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}

# --- CORS : autoriser le frontend Vite en dev ---
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS', 'http://localhost:5173'
).split(',')

# --- Cache / Celery / Channels : Redis (Partie 5) ---
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# Filet de sécurité pour la synchronisation HealthTracker (Partie "notifications") :
# le dispatch normal est immédiat (signal -> envoyer_evenement.delay()), ceci ne
# fait que rattraper les événements en échec ou manqués (Celery hors service au
# moment du signal). Nécessite de lancer, en plus du worker, un process beat :
#   celery -A config beat --loglevel=info
CELERY_BEAT_SCHEDULE = {
    'rattraper-evenements-sync': {
        'task': 'notifications.tasks.traiter_file_evenements',
        'schedule': 300.0,  # toutes les 5 minutes
    },
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {'hosts': [REDIS_URL]},
    }
}

# --- Stockage fichiers : MinIO / S3 (Partie 5), activé seulement si configuré ---
if os.environ.get('USE_S3_STORAGE', 'False') == 'True':
    STORAGES = {
        'default': {'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    }
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'arpenteur')
    AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')  # MinIO en dev
