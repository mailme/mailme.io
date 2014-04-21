from datetime import timedelta

import requests
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from mailme.core.managers import ExtendedManager
from mailme.models.category import Category
from mailme.utils.dates import timedelta_seconds, naturaldate


ACCEPTED_STATUSES = frozenset([requests.codes.OK,
                               requests.codes.FOUND,
                               requests.codes.NOT_MODIFIED,
                               requests.codes.MOVED_PERMANENTLY,
                               requests.codes.TEMPORARY_REDIRECT])

FEED_TIMEDOUT_ERROR = "TIMEDOUT_ERROR"
FEED_NOT_FOUND_ERROR = "NOT_FOUND_ERROR"
FEED_GENERIC_ERROR = "GENERIC_ERROR"

FEED_TIMEDOUT_ERROR_TEXT = _(
    "The feed does not seem to be respond. We will try again later.")
FEED_NOT_FOUND_ERROR_TEXT = _(
    "You entered an incorrect URL or the feed you requested does not exist "
    "anymore.")
FEED_GENERIC_ERROR_TEXT = _(
    "There was a problem with the feed you provided, please check the URL "
    "for mispellings or try again later.")

FEED_ERROR_CHOICES = (
    (FEED_TIMEDOUT_ERROR, FEED_TIMEDOUT_ERROR_TEXT),
    (FEED_NOT_FOUND_ERROR, FEED_NOT_FOUND_ERROR_TEXT),
    (FEED_GENERIC_ERROR, FEED_GENERIC_ERROR_TEXT),
)


class Feed(models.Model):

    """
    An RSS feed.

    .. attribute:: title

        The title of the feed.

    .. attribute:: feed_url

        The URL the feed is located at.

    .. attribute:: description

        The feeds description in full text/HTML.

    .. attribute:: link

        The link the feed says it's located at.
        Can be different from :attr:`feed_url` as it's the
        source we got from the user.

    .. attribute:: date_last_refresh

        Date of the last time this feed was refreshed.

    .. attribute:: last_error

        The last error message (if any).
    """

    title = models.TextField(_("title"))
    feed_url = models.URLField(_("feed URL"), max_length=2048, unique=True)
    # TODO: site_url?
    description = models.TextField(_("description"))
    link = models.URLField(_("link"), max_length=2048, blank=True)
    http_etag = models.CharField(
        _("E-Tag"),
        editable=False,
        blank=True,
        null=True,
        max_length=200
    )
    http_last_modified = models.DateTimeField(
        _("Last-Modified"),
        null=True,
        editable=False,
        blank=True
    )
    date_last_refresh = models.DateTimeField(
        _("date of last refresh"),
        null=True,
        blank=True,
        editable=False
    )
    categories = models.ManyToManyField(Category)
    last_error = models.CharField(
        _("last error"),
        blank=True,
        default="",
        max_length=32,
        choices=FEED_ERROR_CHOICES
    )
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_changed = models.DateTimeField(_("date changed"), auto_now=True)

    is_active = models.BooleanField(_("is active"), default=True)
    freq = models.IntegerField(
        _("frequency"),
        default=settings.MAILME_REFRESH_EVERY
    )

    objects = ExtendedManager()

    class Meta:
        app_label = 'mailme'
        db_table = 'mailme_feed'
        ordering = ("id",)
        verbose_name = _("syndication feed")
        verbose_name_plural = _("syndication feeds")

    def __str__(self):
        return "%s (%s)" % (self.title, self.feed_url)

    def get_posts(self):
        """Get all :class:`Post`s for this :class:`Feed` in order."""
        return self.post_set.order_by('-published')

    def get_post_count(self):
        return self.post_set.count()

    def frequencies(self, limit=None, order="-updated"):
        posts = self.post_set.values("updated").order_by(order)[0:limit]
        frequencies = []
        for idx, post in enumerate(posts):
            frequencies.append(
                posts[idx - 1]['updated'] - post['updated']
            )
        return frequencies

    def average_frequency(self, limit=None, min=5, default=timedelta(hours=2)):
        freqs = self.frequencies(limit=limit)
        if len(freqs) < min:
            return default
        average = sum(map(timedelta_seconds, freqs)) / len(freqs)
        return timedelta(seconds=average)

    def update_frequency(self, limit=None, min=5, save=True):
        self.freq = timedelta_seconds(self.average_frequency(limit, min))
        save and self.save()

    def is_error_status(self, status):
        return (status == requests.codes.NOT_FOUND
                or status not in ACCEPTED_STATUSES)

    def error_for_status(self, status):
        if status == requests.codes.NOT_FOUND:
            return FEED_NOT_FOUND_ERROR
        if status not in ACCEPTED_STATUSES:
            return FEED_GENERIC_ERROR

    def save_error(self, error_msg):
        self._set_last_error = True
        self.last_error = error_msg
        self.save()
        return self

    def save_generic_error(self):
        return self.save_error(FEED_GENERIC_ERROR)

    def save_timeout_error(self):
        return self.save_error(FEED_TIMEDOUT_ERROR)

    def set_error_status(self, status):
        return self.save_error(self.error_for_status(status))

    @property
    def date_last_refresh_naturaldate(self):
        return str(naturaldate(self.date_last_refresh))
