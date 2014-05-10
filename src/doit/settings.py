from doit.conf.development import *

#SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '853034293084-f8oqfjqho6n30m4jk3rmv6mk0v28h4c4.apps.googleusercontent.com'  # noqa
#SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'Pgb6tFneGX0MLaVN6ONH5o4x'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'doit_dev',
        'USER': 'postgres'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
