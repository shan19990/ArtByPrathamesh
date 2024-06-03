"""
Django settings for yaphets project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from decouple import config
import os
from dotenv import load_dotenv, find_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR,"templates")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wecd-et*0#dvsbb5k=5=745opu)(glsyc%1o9zwl4ggu#0sg$('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

SITE_ID = 2


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'marketplace',
    'django_recaptcha',
    'django.contrib.sites',
    "allauth", # new
    "allauth.account", # new
    "allauth.socialaccount", # new
    "allauth.socialaccount.providers.google",
    'allauth.socialaccount.providers.oauth2',
    'imagekit',
]

SOCIALACCOUNT_LOGIN_ON_GET=True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
        'EMAIL_AUTHENTICATION': True,
        'SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT':True,
    }
    
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'yaphets.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'marketplace.context_processors.cart_items_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'yaphets.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR,"staticfiles")

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIAL_AUTH_RAISE_EXCEPTIONS = False
ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_REDIRECT_URL = "landingpage"
LOGOUT_REDIRECT_URL = "landingpage"
ACCOUNT_LOGOUT_ON_GET = True
SOCIAL_AUTH_BACKEND_ERROR_URL = "landingpage"

RECAPTCHA_PUBLIC_KEY = '6LfuwtcpAAAAALw8h1T1EEE1u5xgaSwJRkIKmz-z'
RECAPTCHA_PRIVATE_KEY = '6LfuwtcpAAAAABiXB9hoaQi0B22O1dE9Bl33hA6L'

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


# Load Auth0 application settings into memory
AUTH0_DOMAIN = "dev-c3kko51f2yr255ek.us.auth0.com"
AUTH0_CLIENT_ID = "8zr0N9MOI30Ip7M06KEgDQYx02IgeK04"
AUTH0_CLIENT_SECRET = "qowDbvM7NMk3r3c2R3w8N07rqEH_KNHFBwUIIgMLZElt8LFzXCG5QAMbxEvWu1g8"

# settings.py

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # TLS port
EMAIL_HOST_USER = 'shankhanil.ghosh123@gmail.com'
EMAIL_HOST_PASSWORD = 'ovbxdszhzidoluwt'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
