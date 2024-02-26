"""
Django settings for transcendence project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os	# Added for static files

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '.localhost']


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'transcendence',
	'home',
	'backend',
	'friends',
	'pong',
	'hub',
	'profile',
	'authentication',
	'tournaments_stats',
	'django_htmx',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'transcendence.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			os.path.join(BASE_DIR, 'home', 'templates'),
			os.path.join(BASE_DIR, 'hub', 'templates'),
			os.path.join(BASE_DIR, 'friends', 'templates'),
		],
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

WSGI_APPLICATION = 'transcendence.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
# 	'default': {
# 		'ENGINE': os.getenv('DB_ENGINE'),
# 		'NAME': os.getenv('DB_NAME'),
# 		'USER': os.getenv('DB_USER'),
# 		'PASSWORD': os.getenv('DB_PASSWORD'),
# 		'HOST': os.getenv('DB_HOST'),
# 		'PORT': os.getenv('DB_PORT'),
# 		'OPTIONS': {
# 			'connect_timeout': 300,
# 		}
# 	}
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASE_ROUTERS = ['transcendence.routers.CustomRouter']


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

AUTH_USER_MODEL = 'backend.CustomUser'


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, 'transcendence/static/transcendence'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# 42 API settings

EXTERNAL_API_URL = 'https://api.intra.42.fr/oauth'
EXTERNAL_API_AUTH_URL = os.path.join(EXTERNAL_API_URL, 'authorize')
EXTERNAL_API_TOKEN_URL = os.path.join(EXTERNAL_API_URL, 'token')
EXTERNAL_API_CLIENT_ID = os.getenv('EXTERNAL_API_CLIENT_ID')
EXTERNAL_API_CLIENT_SECRET = os.getenv('EXTERNAL_API_CLIENT_SECRET')
EXTERNAL_API_REDIRECT_URI = 'http://localhost:8000/authentication/auth42/'
EXTERNAL_API_USER_URL = 'https://api.intra.42.fr/v2/me'
EXTERNAL_API_USER_IMAGE_URL = 'https://cdn.intra.42.fr/users/'
EXTERNAL_API_USER_IMAGE_URL_DEFAULT = 'https://cdn.intra.42.fr/users/default.png'
EXTERNAL_API_USER_IMAGE_URL_SMALL = 'https://cdn.intra.42.fr/users/small_'

CORS_ORIGIN_ALLOW_ALL = True


# Default login url name for the login_required decorator
# https://docs.djangoproject.com/en/4.2/topics/auth/default/#the-login-required-decorator

LOGIN_URL = 'login'


SESSION_COOKIE_AGE = 900
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
