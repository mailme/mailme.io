from doit.conf.development import *

SOCIAL_AUTH_MOVES_KEY = '057JETq7x5VMXlhcN8ZtmT1XMs7p4731'  # noqa
SOCIAL_AUTH_MOVES_SECRET = 'GmVWy9gERqfr54E7jFL3SNMtW9RVrlVIkW0OPFK6FE37S15qn4sr764zl9qIAn5L'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'doit_dev',
        'USER': 'postgres'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
