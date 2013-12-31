import os
from datetime import timedelta
from django.conf.global_settings import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, '..')

SECRET_KEY = 'na2p&yexkp-g83$2m^&b!r+a%nv2ci1!d9vh^a_7h!hv*7&h79'

DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mailme',
    'mailme.core',
    'mailme.collector',
    'south',
    'celery',
    'kombu.transport.django',
    'social.apps.django_app.default',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mailme.urls'

WSGI_APPLICATION = 'mailme.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'db.sqlite3'),
    }
}

TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'bower_components'),
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'social.backends.persona.PersonaAuth',
    'social.backends.email.EmailAuth',
    'django.contrib.auth.backends.ModelBackend',
)

#TODO: Already configured here since I think we're going to customize this
#      later either way.
SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL = 'core.User'

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '853034293084-mdami2i23c9dkqopbhfgopdua81croic.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'zoAfLdVkkFvKV4Bo-EwiQPva'

SOCIAL_AUTH_CREATE_USERS = True

# Auth engines and the settings required for them to be listed
AUTH_PROVIDERS = {
    'twitter': ('TWITTER_CONSUMER_KEY', 'TWITTER_CONSUMER_SECRET'),
    'facebook': ('FACEBOOK_APP_ID', 'FACEBOOK_API_SECRET'),
    'google': ('GOOGLE_OAUTH2_CLIENT_ID', 'GOOGLE_OAUTH2_CLIENT_SECRET'),
}

import random

SOCIAL_AUTH_DEFAULT_USERNAME = lambda: random.choice(['Darth Vader', 'Obi-Wan Kenobi', 'R2-D2', 'C-3PO', 'Yoda'])
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email']
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False


LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/done/'
URL_PATH = ''
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_EMAIL_FORM_HTML = 'email_signup.html'
SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'mailme.web.views.send_validation'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = '/email-sent/'
SOCIAL_AUTH_USERNAME_FORM_HTML = 'username_signup.html'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

from django.core.urlresolvers import reverse_lazy
LOGIN_REDIRECT_URL = reverse_lazy('web:login-redirect')

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, '.collected_static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 3 hours
MAILME_REFRESH_EVERY = 3 * 60 * 60
MAILME_POST_LIMIT = 20
MAILME_FEED_TIMEOUT = 10
MAILME_MIN_REFRESH_INTERVAL = timedelta(seconds=60 * 20)

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']

# Queue configuration
from kombu import Queue

BROKER_URL = "django://"

CELERY_ALWAYS_EAGER = True
CELERY_IGNORE_RESULT = True
CELERY_SEND_EVENTS = False
CELERY_RESULT_BACKEND = None
CELERY_TASK_RESULT_EXPIRES = 1
CELERY_DISABLE_RATE_LIMITS = True
CELERY_DEFAULT_QUEUE = "default"
CELERY_DEFAULT_EXCHANGE = "default"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DEFAULT_ROUTING_KEY = "default"
CELERY_CREATE_MISSING_QUEUES = True
CELERY_QUEUES = (
    Queue('default', routing_key='default'),
    Queue('celery', routing_key='celery'),
)

# Disable South in tests as it is sending incorrect create signals
SOUTH_TESTS_MIGRATE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler'
        },
        'sentry': {
            'class': 'raven.contrib.django.handlers.SentryHandler',
        }
    },
    'formatters': {
        'client_info': {
            'format': '%(name)s %(levelname)s %(project_slug)s/%(team_slug)s %(message)s'
        }
    },
    'loggers': {
        '()': {
            'handlers': ['console', 'sentry'],
        },
        'root': {
            'handlers': ['console', 'sentry'],
        },
        'mailme': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'django.request': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}
