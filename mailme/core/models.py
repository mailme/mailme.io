#-*- coding: utf-8 -*-
"""
    mailme.core.models
    ~~~~~~~~~~~~~~~~~~~~~~~
"""
import hashlib
from datetime import datetime, timedelta

import requests
from django.db import models
from django.conf import settings
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _

from mailme.utils.dates import naturaldate
from mailme.core.managers import ExtendedManager

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


def timedelta_seconds(delta):
    """Convert :class:`datetime.timedelta` to seconds.

    Doesn't account for negative values.

    """
    return max(delta.total_seconds(), 0)


class Category(models.Model):
    """Category associated with :class:`Post`` or :class:`Feed`.

    .. attribute:: name

        Name of the category.

    .. attribute:: domain

        The type of category

    """
    name = models.CharField(_("name"), max_length=128)
    domain = models.CharField(_("domain"),
                              max_length=128, null=True, blank=True)

    objects = ExtendedManager()

    class Meta:
        unique_together = ("name", "domain")
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        if self.domain:
            return "%s [%s]" % (self.name, self.domain)
        return "%s" % self.name


class Feed(models.Model):
    """An RSS feed

    .. attribute:: name

        The name of the feed.

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

    name = models.CharField(_("name"), max_length=200)
    feed_url = models.URLField(_("feed URL"), unique=True)
    description = models.TextField(_("description"))
    link = models.URLField(_("link"), max_length=200, blank=True)
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
    freq = models.IntegerField(_("frequency"), default=settings.REFRESH_EVERY)

    objects = ExtendedManager()

    class Meta:
        ordering = ("id",)
        verbose_name = _("syndication feed")
        verbose_name_plural = _("syndication feeds")

    def __str__(self):
        return "%s (%s)" % (self.name, self.feed_url)

    def get_posts(self):
        """Get all :class:`Post`s for this :class:`Feed` in order."""
        return self.post_set.order_by('-date_published')

    def get_post_count(self):
        return self.post_set.count()

    def frequencies(self, limit=None, order="-date_updated"):
        posts = self.post_set.values("date_updated").order_by(order)[0:limit]
        frequiencies = []
        for idx, post in enumerate(posts):
            frequencies.append(
                posts[idx - 1]['date_updated'] - post['date_updated']
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


class Enclosure(models.Model):
    """Media enclosure for a Post

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
        verbose_name = _("enclosure")
        verbose_name_plural = _("enclosures")

    def __str__(self):
        return "%s %s (%d)" % (self.url, self.type, self.length)


class Post(models.Model):
    """A Post for an RSS feed

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

    .. attribute:: date_published

        The date this post was published.

    .. attribute:: date_updated

        The date this post was last changed/updated.

    .. attribute:: enclosures

        List of media attachments for this post.

    """

    feed = models.ForeignKey(Feed, null=False, blank=False)
    title = models.CharField(_("title"), max_length=200)

    # using 2048 for long URLs
    link = models.URLField(_("link"), max_length=2048)
    content = models.TextField(_("content"), blank=True)
    guid = models.CharField(_("guid"), max_length=200, blank=True)
    author = models.CharField(_("author"), max_length=50, blank=True)
    date_published = models.DateField(_("date published"))
    date_updated = models.DateTimeField(_("date updated"))
    enclosures = models.ManyToManyField(Enclosure, blank=True)
    categories = models.ManyToManyField(Category)

    objects = ExtendedManager()

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def auto_guid(self):
        """Automatically generate a new guid from the metadata available."""
        payload = (self.title, self.link, self.author)
        return hashlib.md5("|".join(payload).encode('utf-8')).hexdigest()

    def __str__(self):
        return "%s" % self.title

    @property
    def date_published_naturaldate(self):
        date = self.date_published
        as_datetime = datetime(date.year, date.month, date.day, tzinfo=utc)
        return str(naturaldate(as_datetime))

    @property
    def date_updated_naturaldate(self):
        return str(naturaldate(self.date_updated))
