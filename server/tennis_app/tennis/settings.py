"""
Django settings for tennis project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from celery.schedules import crontab
import tennis.tasks
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=va1+ylh)j3#575f2u36lbf4n#k8n7fv5n55a2@-)p)s)s3-e8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', 'tennis57.ru']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'rest_framework',
    'django_admin_filters',

]

MIDDLEWARE = [
    #'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tennis.urls'

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

WSGI_APPLICATION = 'tennis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES_setting = {
#     'default': {
#         "ENGINE":'django.db.backends.postgresql_psycopg2', # os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
#         "NAME":'tennis_db',# os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
#         "USER": 'tennis_user', # os.environ.get("SQL_USER", "user"),
#         "PASSWORD": 'tennis_user', # os.environ.get("SQL_PASSWORD", "password"),
#         "HOST": 'db', # os.environ.get("SQL_HOST", "localhost"),
#         "PORT": os.environ.get("SQL_PORT", "5432"),
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'tennis_db',
#         'USER': 'tennis_user',
#         'PASSWORD': 'tennis_user',
#         'HOST': 'db',
#         'PORT': os.environ.get("SQL_PORT", "5432"),
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# EMAIL_USE_TLS = True
# # EMAIL_USE_SSL = False
# EMAIL_HOST = 'smtp.mail.ru'
# EMAIL_PORT = 2525
# EMAIL_HOST_USER = 'tennis57@bk.ru'
# EMAIL_HOST_PASSWORD = 'cumnwzF47NKwAEnBxiHs'
# SERVER_EMAIL = EMAIL_HOST_USER
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'misha.homi@gmail.com'
EMAIL_HOST_PASSWORD = 'yrvsctiipzcibetb'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


LOGIN_REDIRECT_URL = '/'

CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "tennis.tasks.sample_task",
        "schedule": crontab(minute="*/1"),
    },
}


CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
