from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MailmeConfig(AppConfig):
    name = 'mailme'
    verbose_name = _('Mailme')

    def ready(self):
        # We do like our application structure more than django's
        # so we import our modules manually.
        from mailme.models import user, category, enclosure, feed, post  # noqa
