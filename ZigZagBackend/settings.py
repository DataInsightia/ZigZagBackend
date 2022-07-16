from operator import truediv
import environ
from pathlib import Path
import os
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()
# env = environ.Env(
#     DEBUG=(bool, False)
# )
# environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
DEBUG = True
if DEBUG:
    SECRET_KEY = "django-insecure-wkfnk!(o%9e%)q0+1=@c9m@b16r$3owh=#0(0-bciluq$6o&h-"
    ALLOWED_HOSTS = ["*"]
else:
    SECRET_KEY = env('SECRET_KEY')
    ALLOWED_HOSTS = env('ALLOWED_HOSTS')

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "api",
    "corsheaders",
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]
AUTH_USER_MODEL = 'api.User'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    # 'DEFAULT_RENDERER_CLASSES': [
    #     'rest_framework.renderers.JSONRenderer',
    # ]

}
ROOT_URLCONF = "ZigZagBackend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "ZigZagBackend.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

OFFLINE = True

if OFFLINE:
    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.sqlite3",
    #         "NAME": "db.sqlite3",
    #     }
    # }
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'db',
        # 'PORT': 3306,
    }
}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'dataioit_zigzag',
            'USER': 'dataioit_zigzag',
            'PASSWORD': '@zigzag123',
            'HOST': 'localhost',
            'OPTIONS' : {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            }
        }
    }


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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True



STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media') 
MEDIA_URL = '/media/'

TIME_ZONE = "Asia/Kolkata"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ORIGIN_ALLOW_ALL = True

if DEBUG:
    CORS_ALLOW_CREDENTIALS = True
    CSRF_TRUSTED_ORIGINS = ["https://chettinadzigzag.in"]
else:
    CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS')
    SECURE_HSTS_SECONDS = 31536000 
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECRET_KEY_MIN_LENGTH = 10
    SECRET_KEY_MIN_UNIQUE_CHARACTERS = 20
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_REFERRER_POLICY = 'strict-origin'
    SECURE_BROWSER_XSS_FILTER = True

