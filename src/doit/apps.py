from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DoitConfig(AppConfig):
    name = 'doit'
    verbose_name = _('Doit')

    def ready(self):
        # We do like our application structure more than django's
        # so we import our modules manually.
        from doit.models import user  # noqa
