"""
    For more information on this file, see
    https://docs.djangoproject.com/en/1.8/topics/settings/

    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/1.8/ref/settings/

    Needs some environment strings in the live server.

        LIVE -- To know its in the live server.
        SECRET_KEY -- The secret key to be used.
        STEAM_API_KEY -- The key needed to use the steam web api.
"""

from django.urls import reverse_lazy
import os.path


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) )


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get( 'LIVE' ):
    DEBUG = False

else:
    DEBUG = True


# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = 'hai'

else:
    SECRET_KEY = os.environ[ 'SECRET_KEY' ]


if DEBUG:
    with open( os.path.join( BASE_DIR, 'steam/steam_api_key.txt' ), 'r', encoding= 'utf-8' ) as f:
        STEAM_API_KEY = f.read()

else:
    STEAM_API_KEY = os.environ[ 'STEAM_API_KEY' ]


# Hosts/domain names that are valid for this site; required if DEBUG is False
if not DEBUG:
    ALLOWED_HOSTS = [ 's-web-api.herokuapp.com' ]


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'social_django',

    'accounts',
    'steam',
)


MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'steam.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join( BASE_DIR, 'templates' ),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]


# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'steam.wsgi.application'


# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join( BASE_DIR, 'db.sqlite3' ),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join( BASE_DIR, 'static_root' )


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join( BASE_DIR, 'static' ),
)


LOGIN_URL = reverse_lazy( 'social:begin', args=[ 'steam' ] )
LOGOUT_URL = 'accounts:logout'
LOGIN_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'accounts.Account'


AUTHENTICATION_BACKENDS = (
    'social_core.backends.steam.SteamOpenId',
    'django.contrib.auth.backends.ModelBackend',
)


SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = [ 'username', 'first_name', 'email' ]
SOCIAL_AUTH_STEAM_API_KEY = STEAM_API_KEY
SOCIAL_AUTH_STEAM_EXTRA_DATA = [ 'player' ]
SOCIAL_AUTH_USER_MODEL = 'accounts.Account'


SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'accounts.auth_pipeline.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)


if not DEBUG:

    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES[ 'default' ] =  dj_database_url.config()

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ( 'HTTP_X_FORWARDED_PROTO', 'https' )