from django.db import models
from django.utils.translation import ugettext_lazy as _

from mailme.core.managers import ExtendedManager


class Category(models.Model):
    """Category associated with :class:`Post`` or :class:`Feed`.

    .. attribute:: title

        Title of the category.

    .. attribute:: domain

        The type of category

    """
    title = models.CharField(_("title"), max_length=200)
    domain = models.CharField(
        _("domain"),
        max_length=200,
        null=True,
        blank=True
    )

    objects = ExtendedManager()

    class Meta:
        app_label = 'mailme'
        db_table = 'mailme_category'
        unique_together = ("title", "domain")
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        if self.domain:
            return "%s [%s]" % (self.title, self.domain)
        return "%s" % self.title
