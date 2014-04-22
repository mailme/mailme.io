from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from mailme.utils.imports import import_submodules


class MailmeConfig(AppConfig):
    name = 'mailme'
    verbose_name = _('Mailme')

    def ready(self):
        # We do like our application structure more than django's
        # so we import our modules manually.
        from mailme import models
        import_submodules(models, models.__name__, models.__path__)
