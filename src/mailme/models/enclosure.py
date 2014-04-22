from django.db import models
from django.utils.translation import ugettext_lazy as _

from mailme.core.managers import ExtendedManager


class Enclosure(models.Model):
    """
    Media enclosure for a Post.

    .. attribute:: url

        The location of the media attachment.

    .. attribute:: type

        The mime/type of the attachment.

    .. attribute:: length

        The actual content length of the file
        pointed to at :attr:`url`.
    """
    url = models.URLField(_("URL"))
    type = models.CharField(_("type"), max_length=200)
    length = models.PositiveIntegerField(_("length"), default=0)

    objects = ExtendedManager()

    class Meta:
        app_label = 'mailme'
        verbose_name = _("enclosure")
        verbose_name_plural = _("enclosures")

    def __str__(self):
        return "%s %s (%d)" % (self.url, self.type, self.length)
