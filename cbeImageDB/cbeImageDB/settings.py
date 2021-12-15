"""
Django settings for cbeImageDB project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os, re
from decouple import config


# If it is running on heroku get db credentals how heroku requires, otherwise
# get from environment .env file
DOCKER_BUILDING = os.environ.get('DOCKER_BUILDING', '')
RUN_LOCATION = os.environ.get('RUN_LOCATION', "").lower()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'default')

# SECURITY WARNING: don't run with debug turned on in production!
debug_val = os.environ.get('DJANGO_DEBUG', 'False')
if debug_val.lower() == 'true':
    DEBUG = True
elif debug_val.lower() == 'false':
    DEBUG = False


# Use an environment variable to create the list
# of hosts. It should be separated by commas
ALLOWED_HOSTS = []
web_allowed_hosts = os.environ.get('WEB_ALLOWED_HOSTS', '')
print('*********************************************************************')
print('*********************************************************************')
print('******{}**********************************'.format(web_allowed_hosts))
print('*********************************************************************')
print('*********************************************************************')
print('*********************************************************************')
print('*********************************************************************')
for host in web_allowed_hosts.split(','):
    ALLOWED_HOSTS.append(host)


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'images.apps.ImagesConfig',
    'dal',
     # Enable plugins
    'dal_select2',
    'admin_views',
    'django_elasticsearch_dsl',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'easy_thumbnails',
    'crispy_forms',
]


if DOCKER_BUILDING != '':
    # make blank becuase do not need while building docker container
    ELASTICSEARCH_DSL = {}
elif RUN_LOCATION == 'heroku':
    # get the url for elasticsearch from Heroku's variable
    bonsai_url = os.environ.get("SEARCHBOX_URL", "")
    # if bonsai_url is empty on Heroku, it is building the container
    ELASTICSEARCH_DSL={
        'default': {
            'hosts': bonsai_url
        },
    }
else:
    # using .env file
    ELASTICSEARCH_DSL={
        'default': {
            'hosts': '{}:9200'.format(os.environ['ELASTIC_HOST'])
        },
    }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # whitenoise is supposed to do static while DEBUG=False
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # add it exactlyhere
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cbeImageDB.urls'

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

THUMBNAIL_ALIASES = {
    'images': {
        'list': {'size': (200, 200),},
        'details': {'size': (350, 350),}
    },
}

WSGI_APPLICATION = 'cbeImageDB.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


# put here so will initilize for collectstatic in Dockerfile
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "",
        'USER': "",
        'PASSWORD': "",
        'HOST': "",
        'PORT': "",
    }
}

if DOCKER_BUILDING != "":
    pass
elif RUN_LOCATION == 'heroku':
    # Heroku: Update database configuration from $DATABASE_URL.
    import dj_database_url
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASS'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
        }
    }

'''
'''

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = config('STATIC_ROOT')
STATIC_ROOT = os.environ.get('STATIC_ROOT')

# Path for storing files
#MEDIA_ROOT = config('MEDIA_ROOT')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '')
MEDIA_URL = '/files/'

#SYNONYM_FILE = config('SYNONYM_FILE')

# cloudinary stuff for heroku file storage
CLOUD_NAME = os.environ.get('CLOUD_NAME', '')
#cloudinary://271569232542553:oa-O-S-nIww8dEyIym4HyHQO3CY@hcvvcmoo7
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL', '')
if CLOUDINARY_URL != '':
    # only add these if needed becuase during collect static in Dockerfile,
    # having them seems to mess things up
    INSTALLED_APPS.append('cloudinary_storage')
    INSTALLED_APPS.append('cloudinary')

    # split up url in form of
    # cloudinary://api_key:api_secret@cloud_name
    blah, api_key, api_secret, cloud_name = re.split('://|:|@', CLOUDINARY_URL)

    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': cloud_name,
        'API_KEY': api_key,
        'API_SECRET': api_secret,
    }

    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
