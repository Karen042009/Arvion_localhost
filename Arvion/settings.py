import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# --- CORE SETTINGS & ENVIRONMENT LOADING ---
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-safe-secret-key-for-local-use-only')
DEBUG = os.environ.get('DEBUG', '0') == '1'
ROOT_URLCONF = "Arvion.urls"
WSGI_APPLICATION = "Arvion.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "main.CustomUser"

# --- SECURITY & HOSTS ---
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

# --- INSTALLED APPS & MIDDLEWARE ---
INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages",
    "whitenoise.runserver_nostatic", "django.contrib.staticfiles",
    'cloudinary_storage', 'cloudinary', "main.apps.MainConfig",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware", "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- TEMPLATES & INTERNATIONALIZATION ---
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [os.path.join(BASE_DIR, "templates")], "APP_DIRS": True,
    "OPTIONS": {"context_processors": ["django.template.context_processors.debug", "django.template.context_processors.request", "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages",],},},]
LANGUAGE_CODE = "en-us"; TIME_ZONE = "UTC"; USE_I18N = True; USE_TZ = True

# --- DATABASES ---
if 'DATABASE_URL' in os.environ:
    DATABASES = {'default': dj_database_url.config(conn_max_age=600, ssl_require=True)}
else:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}

# --- STATIC & MEDIA FILES ---
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")] # <-- Ավելացված կարևոր տողը
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
if 'CLOUDINARY_URL' in os.environ:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    CLOUDINARY_STORAGE = {'CLOUDINARY_URL': os.environ.get('CLOUDINARY_URL')}
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- PASSWORDS & API KEYS ---
AUTH_PASSWORD_VALIDATORS = [{"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},{"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},{"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},{"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},]
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')