"""
Django settings for base project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = bool(os.environ.get("DEBUG", default=0))

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS='localhost' '127.0.0.1' [::1]'
#ALLOWED_HOSTS=['localhost', '127.0.0.1', '[::1]']
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # add here the app names
    'django_q',
    'website',
    'backoffice',
    'gold_bi',
    'fontawesomefree',
    'logging_app',
    'pwa',
    'webpush',
    'django_seed',


]



MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'logging_app.middleware.LogMiddleware',
]

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("POSTGRES_DB", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("POSTGRES_USER", "user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    },
    'gold': {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("GOLD_POSTGRES_DB", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("GOLD_POSTGRES_USER", "user"),
        "PASSWORD": os.environ.get("GOLD_POSTGRES_PASSWORD", "password"),
        "HOST": os.environ.get("GOLD_SQL_HOST", "localhost"),
        "PORT": os.environ.get("GOLD_SQL_PORT", "5432"),
    }
}
   



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
#STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/backoffice/'
LOGOUT_REDIRECT_URL = '/'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 102400000000
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://*:8000", "https://" + os.environ.get("DOMAIN").split(' ')[0], "https://" + os.environ.get("DOMAIN").split(' ')[1]]



PWA_APP_NAME = "ARNIA"
PWA_APP_DESCRIPTION = "app for website and financial tracking"
PWA_APP_THEME_COLOR = "#5d8afc"
PWA_APP_BACKGROUND_COLOR = "#1e5cfa"
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': "/static/pwa/icons/icon-256x256.png",
        'sizes': '256x256'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': "/static/pwa/icons/icon-512x512.png",
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]



# settings.py
Q_CLUSTER = {
    'name': 'gold_bi',
    'workers': 4,
    'recycle': 500,
    'timeout': 60,
    'django_redis': 'default',
    'retry': 3600,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {name} {levelname} {pathname}:{lineno} - {funcName}() - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file_schedules': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'schedules.log'),
            'formatter': 'verbose',
        },
        'file_tasks': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'tasks.log'),
            'formatter': 'verbose',
        },
        'file_reports': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'reports.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'schedules': {
            'handlers': ['file_schedules'],
            'level': 'INFO',
            'propagate': True,
        },
        'tasks': {
            'handlers': ['file_tasks'],
            'level': 'INFO',
            'propagate': True,
        },
        'reports': {
            'handlers': ['file_reports'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
