import os
from datetime import timedelta
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, '..')

SECRET_KEY = 'na2p&yexkp-g83$2m^&b!r+a%nv2ci1!d9vh^a_7h!hv*7&h79'

DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mailme',

    'suit',
    'django.contrib.admin',

    'social.apps.django_app.default',

    'celery',
    'kombu.transport.django',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mailme.middlewares.social.SocialAuthExceptionMiddleware',
)

ROOT_URLCONF = 'mailme.urls'

WSGI_APPLICATION = 'mailme.wsgi.application'

AUTH_USER_MODEL = 'mailme.User'

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
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.github.GithubOAuth2',
    'social.backends.username.UsernameAuth',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = reverse_lazy('mailme-index')
LOGIN_ERROR_URL = reverse_lazy('mailme-index')
LOGIN_REDIRECT_URL = reverse_lazy('mailme-index')

SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'

SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_SANITIZE_REDIRECTS = True
SOCIAL_AUTH_USER_FIELDS = ('username', 'email', 'password')
SOCIAL_AUTH_REQUIRED_USER_FIELDS = ('username', 'email')
SOCIAL_AUTH_PROTECTED_USER_FIELDS = SOCIAL_AUTH_REQUIRED_USER_FIELDS

SOCIAL_AUTH_PIPELINE = (
    'mailme.pipeline.unique_login',
    'mailme.pipeline.conditional_social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.social_user',
    'mailme.pipeline.require_user_details',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'mailme.pipeline.email_verification',
)

SOCIAL_AUTH_USERNAME_FORM_URL = reverse_lazy('mailme-index')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_GITHUB_KEY = ''
SOCIAL_AUTH_GITHUB_SECRET = ''


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

# Celery / Queue configuration
from kombu import Queue

BROKER_URL = "django://"

# Per default process all celery tasks in-process.
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# Only accept JSON. This will be the default in Celery 3.2
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

# Explicitly set default queue and exchange types. This is only useuseful for
# RabbitMQ but still good to have as a general rule.
CELERY_DEFAULT_QUEUE = "default"
CELERY_DEFAULT_EXCHANGE = "default"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DEFAULT_ROUTING_KEY = "default"
CELERY_CREATE_MISSING_QUEUES = True

# Track started tasks. This adds a new STARTED state once a task
# is started by the celery worker.
CELERY_TRACK_STARTED = True

CELERY_QUEUES = (
    Queue('default', routing_key='default'),
    Queue('celery', routing_key='celery'),
)

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERYBEAT_MAX_LOOP_INTERVAL = 3600
CELERY_DISABLE_RATE_LIMITS = True

# Make our `LOGGING` configuration the only truth and don't let celery
# overwrite it.
CELERYD_HIJACK_ROOT_LOGGER = False

# Don't log celery log-redirection as warning (default).
# We manage our logging through `django.conf.settings.LOGGING` and
# want that to be our first-citizen config.
CELERY_REDIRECT_STDOUTS_LEVEL = 'INFO'

# Disable South in tests as it is sending incorrect create signals
SOUTH_TESTS_MIGRATE = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.handlers.SentryHandler',
            'formatter': 'simple'
        }
    },
    'formatters': {
        'verbose': {
            'format':
                '[%(asctime)s] %(levelname)s:%(name)s %(funcName)s\n %(message)s',  # noqa
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'loggers': {
        # This is the root logger that catches everything, if there's no other
        # match on the logger name. If we want custom logging handing for our
        # code vs. third-party code, define loggers for each module/app
        # that's using standard python logging.
        'root': {
            'level': 'INFO',
            'handlers': ['console'],
        },
        'celery': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'mailme': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
