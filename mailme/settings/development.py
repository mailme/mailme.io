from mailme.settings.base import *

# Uncomment and edit

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '853034293084-mdami2i23c9dkqopbhfgopdua81croic.apps.googleusercontent.com'  # noqa
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'zoAfLdVkkFvKV4Bo-EwiQPva'

SOCIAL_AUTH_TWITTER_KEY = 'YKQRADpaOw9TFBqvV7C6L1Lp6'
SOCIAL_AUTH_TWITTER_SECRET = 'u0lNNL24IVaXb3nN58BjMH0YCCdVRZ24CzLnUnr9iBEka7FzJ6'

SOCIAL_AUTH_FACEBOOK_KEY = '279997472164576'
SOCIAL_AUTH_FACEBOOK_SECRET = '048d502be521836de9e453e0a6f068fd'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_GITHUB_KEY = '087b8ad20f3d34f9989d'
SOCIAL_AUTH_GITHUB_SECRET = '9a09a683be98023a8177980dd124dd24d5ef3588'


LOGGING['loggers']['root']['level'] = 'DEBUG'
LOGGING['loggers']['celery']['level'] = 'DEBUG'
LOGGING['loggers']['mailme']['level'] = 'DEBUG'
