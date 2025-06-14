import os
from warnings import warn
from pathlib import Path
from django.core.management.utils import get_random_secret_key


CELERY_BROKER_URL = "redis://localhost:6379/0"
DBNAME = os.getenv("DBNAME") or warn(
    "No Database Name set in environment variable DBNAME"
)
DBUSER = os.getenv("DBUSER") or warn(
    "No Database User set in environment variable DBUSER"
)
DBPASSWORD = os.getenv("DBPASSWORD") or warn(
    "No Database Password set in environment variable DBPASSWORD"
)
DBHOST = os.getenv("DBHOST") or warn(
    "No Database Host set in environment variable DBHOST"
)

GMAP_APIKEY = os.getenv("GMAP_APIKEY") or warn(
    "You need to set a GMAP_APIKEY environment variable"
)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
HOUSEMAP = f"{BASE_DIR}/data/tl_2023_22_sldl.shp"
SENATEMAP = f"{BASE_DIR}/data/tl_2023_22_sldu.shp"
NOLACOUNCILMAP = f"{BASE_DIR}/data/City_Council_Districts.shp"
CONGRESSMAP = f"{BASE_DIR}/data/Congressional_Districts.shp"
HOUSEMEMBERS = f"{BASE_DIR}/data/HouseMembers.csv"
SENATEMEMBERS = f"{BASE_DIR}/data/SenateMembers.csv"
HOUSEMEMBERBASEURL = f"https://house.louisiana.gov/H_Reps/members?ID="
SENATEMEMBERBASEURL = f"https://senate.la.gov/smembers?ID="
SUPPORTED_STATES = ["Louisiana"]
IGNORED_UAS = os.getenv("IGNORED_UAs") or [
    "Mozilla/5.0 (compatible; Uptime/1.0; http://uptime.com)",
]

IGNORED_IPS = os.getenv("IGNORED_IPS") or []
TEMPLATE_DIRS = [f"{BASE_DIR}/LALookup/templates/"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY") or get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv("DEBUG")) or False


ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "action.defendlouisiana.org",
    "lookup.defendlouisiana.org",
    "lalookup-530602149581.herokuapp.com",
]


# Application definition

INSTALLED_APPS = [
    "LALookup",
    "bootstrap5",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_bootstrap_icons",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # 'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "LALookup.middleware.SaveRequest",
]

ROOT_URLCONF = "LALookup.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": TEMPLATE_DIRS,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "LALookup.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": DBNAME,
        "USER": DBUSER,
        "PASSWORD": DBPASSWORD,
        "HOST": DBHOST,
        "PORT": "5432",
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"
# TIME_ZONE = 'UTC'
TIME_ZONE = "America/Chicago"
USE_TZ = True
USE_I18N = True

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_HOST = os.environ.get("DJANGO_STATIC_HOST", "")
STATIC_URL = STATIC_HOST + "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
