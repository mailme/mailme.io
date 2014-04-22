from datetime import datetime
import hashlib

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from mailme.core.managers import ExtendedManager
from mailme.models.feed import Feed
from mailme.models.enclosure import Enclosure
from mailme.models.category import Category
from mailme.utils.dates import naturaldate


class Post(models.Model):

    """
    A Post for an RSS feed.

    .. attribute:: feed

        The feed which this is a post for.

    .. attribute:: title

        The title of the post.

    .. attribute:: link

        Link to the original article.

    .. attribute:: content

        The posts content in full-text/HTML.

    .. attribute:: guid

        The GUID for this post (unique for :class:`Feed`)

    .. attribute:: author

        Name of this posts author.

    .. attribute:: published

        The date this post was published.

    .. attribute:: updated

        The date this post was last changed/updated.

    .. attribute:: enclosures

        List of media attachments for this post.
    """

    feed = models.ForeignKey(Feed, null=False, blank=False)
    title = models.TextField(_("title"))

    # using 2048 for long URLs
    link = models.URLField(_("link"), max_length=2048)
    content = models.TextField(_("content"), blank=True)
    # TODO: Save `summary` separate.
    guid = models.CharField(_("guid"), max_length=2048, blank=True)
    author = models.TextField(_("author"), blank=True)
    published = models.DateTimeField(_("date published"), default=timezone.now)
    updated = models.DateTimeField(_("date updated"), default=timezone.now)

    enclosures = models.ManyToManyField(Enclosure, blank=True)
    categories = models.ManyToManyField(Category)

    objects = ExtendedManager()

    class Meta:
        app_label = 'mailme'
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def auto_guid(self):
        """Automatically generate a new guid from the metadata available."""
        payload = (self.title, self.link, self.author)
        return hashlib.md5("|".join(payload).encode('utf-8')).hexdigest()

    def __str__(self):
        return "%s" % self.title

    @property
    def published_naturaldate(self):
        date = self.published
        as_datetime = datetime(
            date.year,
            date.month,
            date.day,
            tzinfo=timezone.utc
        )
        return str(naturaldate(as_datetime))

    @property
    def updated_naturaldate(self):
        return str(naturaldate(self.updated))
