"""
Django settings for lasantabiblia project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from datetime import timedelta

import os
from dotenv import load_dotenv
# This makes the values accessible.
load_dotenv()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=*@sf%07zlfb-w-1owu04$2cnnsc4l(cz1az-t31(54^k_j_e^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'SyncUp',
    'Resources',
    'Core',
    'RestAPIS',
    'Auth',
    'Account',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',#generates 2 models, outstanding and blacklist for Refresh tokens
    'django_cleanup.apps.CleanupConfig', # clean media files when removed from db
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#REST FRAMEWORK SPECIFIC
# The default permission is ‘rest_framework.permissions.AllowAny’, which – as the name suggests – allows everyone to do anything. 
# Let’s protect the API so that only logged-in users have access. by adding the following entry:
# DEFAULT_AUTHENTICATION_CLASSES -> used if no authentication_classes provided
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

#SIMPLE_JWT SPECIFIC
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(weeks=5),
    'ROTATE_REFRESH_TOKENS': True, # RETURN new Refresh token and access token when TokenRefreshView
    'BLACKLIST_AFTER_ROTATION': True, # Refresh tokens submitted to the TokenRefreshView to be added to the blacklist. 
}

ROOT_URLCONF = 'lasantabiblia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'lasantabiblia.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
#os.environ.get('NAME_OF_ENV') -> GET environmnet variables
DATABASES = {
    'default': {
        'ENGINE': os.getenv("MYSQL_ENGINE"),
        'NAME': os.getenv("MYSQL_NAME"),
        'USER': os.getenv("MYSQL_USER"),
        'PASSWORD': os.getenv("MYSQL_PASSWORD"),
        'HOST': os.getenv("MYSQL_HOST"),
        'PORT': os.getenv("MYSQL_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# When you deploy your application, we run 'python manage.py collecstatics' and if it has a static folder,
# it will collect and put the files into a folder in the ROOT.
# WE DEFINE THE NAME OF THE FOLDER HERE:
STATIC_ROOT= os.path.join(BASE_DIR, 'static') # make sure to .gitignore this folder
# URL for us to access the files
STATIC_URL = '/static/'
# location of the static folder THAT WE ARE GOING TO USE. e.g: inside the Root project
# so we can reference static files using HTML template: {% static 'img/bible.png' %}
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'lasantabiblia/static')
]

#ADD THIS SO YOU CAN MAKE YOUR PROJECT AVAILABLE TO YOUR HOME NETWORK:
#THEN, it can be access through your phone
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.0.14']#ADD YOUR IP HERE.

#reference the App/ModelClassName -> tell Django that we want to use a Custom model for the built-in User table
AUTH_USER_MODEL = 'Account.Account'

# Images|media added during runtime.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#FOR DEPLOYMENT=================================================================
try:
    from .local_settings import * #IMPORT this file if it exists
except ImportError:
    pass