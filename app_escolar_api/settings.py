import os
from pathlib import Path
from dotenv import load_dotenv   # necesitas tener instalado python-dotenv

# ==========================
# RUTAS / .ENV
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables desde .env (en la misma carpeta que manage.py)
load_dotenv(BASE_DIR / '.env')

# ==========================
# CONFIGURACIÓN BÁSICA
# ==========================

# Si en .env existe SECRET_KEY la toma, si no usa la que ya tenías
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    '-_&+lsebec(whhw!%n@ww&1j=4-^j_if9x8$q778+99oz&!ms2'
)

# En producción en PythonAnywhere pon DEBUG=False en tu .env
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# En .env puedes poner:
# ALLOWED_HOSTS=localhost,127.0.0.1,ivanflores387.pythonanywhere.com
ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1,ivanflores387.pythonanywhere.com'
).split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',                 # necesarios para los filtros de DRF
    'rest_framework',
    'rest_framework.authtoken',       # conserva soporte de tokens de DRF
    'corsheaders',                    # librería CORS actualizada
    'app_escolar_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',     # CORS debe ir antes de CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==========================
# CORS
# ==========================

# En tu .env puedes poner:
# CORS_ALLOWED_ORIGINS=https://sistema-web-app.vercel.app,http://localhost:4200
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'https://sistema-web-app.vercel.app,http://localhost:4200'
).split(',')

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'app_escolar_api.urls'

# ==========================
# TEMPLATES / STATIC / MEDIA
# ==========================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = "/static/"

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

WSGI_APPLICATION = 'app_escolar_api.wsgi.application'

# ==========================
# BASE DE DATOS (MySQL)
# ==========================
# En tu .env de PythonAnywhere:
# DB_NAME=ivanflores387$App_Web_Api
# DB_USER=ivanflores387
# DB_PASSWORD=TU_PASSWORD_MYSQL
# DB_HOST=ivanflores387.mysql.pythonanywhere-services.com
# DB_PORT=3306

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'ivanflores387$App_Web_Api'),
        'USER': os.getenv('DB_USER', 'ivanflores387'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),  # pon la contraseña en el .env
        # MUY IMPORTANTE: por defecto usa el host de PythonAnywhere, NO 127.0.0.1
        'HOST': os.getenv('DB_HOST', 'ivanflores387.mysql.pythonanywhere-services.com'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# ==========================
# AUTH / I18N / DRF
# ==========================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'app_escolar_api.models.BearerTokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}
