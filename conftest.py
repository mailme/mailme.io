from django.conf import settings
import os
import os.path


def pytest_configure(config):
    if not settings.configured:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'doit.conf.test'

    test_db = os.environ.get('DB', 'postgres')
    if test_db in ('mysql', 'sqlite'):
        raise RuntimeError('not supported')
    elif test_db == 'postgres':
        settings.DATABASES['default'].update({
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'postgres',
            'NAME': 'doit_test',
        })

    # override a few things with our test specifics
    settings.INSTALLED_APPS = tuple(settings.INSTALLED_APPS) + (
        'doit.tests',
    )
