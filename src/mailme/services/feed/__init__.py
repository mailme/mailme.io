# -*- coding: utf-8 -*-
"""
    mailme.services.feed
    ~~~~~~~~~~~~~~~~~~~~

    Add support for:

     * Opml
     * RSS / Atom
     * Basically everything that `feedparser` supports.
"""
import time
import socket
import hashlib
from datetime import datetime, timedelta

import listparser
import requests
import feedparser
import pytz
from requests import codes
from django.conf import settings
from django.utils.timezone import utc
from django.utils.encoding import force_text, force_bytes

from mailme import exceptions
from mailme.services.base import BaseService
from mailme.models.feed import (
    Feed,
    ACCEPTED_STATUSES,
    FEED_GENERIC_ERROR_TEXT,
    FEED_TIMEDOUT_ERROR_TEXT,
    FEED_NOT_FOUND_ERROR_TEXT
)

from mailme.models.post import Post
from mailme.models.category import Category
from mailme.models.enclosure import Enclosure
from mailme.utils.html import cleanup_html
from mailme.utils.logging import logged


GUID_FIELDS = frozenset(("title", "link", "author"))


def find_post_content(feed_obj, entry):
    try:
        content = entry["content"][0]["value"]
    except (IndexError, KeyError):
        content = entry.get("description") or entry.get("summary") or ""
    return cleanup_html(content)


def date_to_datetime(field_name):
    """Given a post field, convert its :mod:`feedparser` date tuple to
    :class:`datetime.datetime` objects.

    :param field_name: The post field to use.

    """

    def _field_to_datetime(feed_obj, entry):
        if field_name in entry:
            try:
                time_ = time.mktime(entry[field_name])
                date = datetime.fromtimestamp(time_).replace(tzinfo=utc)
            except TypeError:
                date = datetime.now(pytz.utc)
            return date
        return datetime.now(pytz.utc)
    _field_to_datetime.__doc__ = "Convert %s to datetime" % repr(field_name)

    return _field_to_datetime


def generate_guid(entry):
    """Generate missing guid for post entry."""
    text = "|".join(force_text(entry.get(key) or "") for key in GUID_FIELDS)
    return hashlib.md5(force_bytes(text)).hexdigest()


def get_entry_guid(feed_obj, entry):
    """
    Get the guid for a post.

    If the post doesn't have a guid, a new guid is generated.
    """
    if "guid" not in entry:
        return generate_guid(entry)

    guid = force_text(entry["guid"]).strip()
    return guid


def format_date(t):
    """Make sure time object is a :class:`datetime.datetime` object."""
    if isinstance(t, time.struct_time):
        return datetime(*t[:6], tzinfo=pytz.utc)
    return t.replace(tzinfo=utc)


def entries_by_date(entries, limit=None):
    """
    Sort the feed entries by date.

    :param entries: Entries given from :mod:`feedparser``.
    :param limit: Limit number of posts.
    """
    now = datetime.now(pytz.utc)

    def find_date(entry, counter):
        """Find the most current date entry tuple."""

        return (entry.get("published_parsed") or
                entry.get("date_parsed") or
                now - timedelta(seconds=(counter * 30)))

    sorted_entries = []
    for counter, entry in enumerate(entries):
        date = format_date(find_date(entry, counter))
        # the found date is put into the entry
        # because some feed just don't have any valid dates.
        # This will ensure that the posts will be properly ordered
        # later on when put into the database.
        entry["published_parsed"] = (entry.get("published_parsed")
                                     or date.timetuple())
        sorted_entries.append((date, entry))

    sorted_entries.sort(key=lambda key: key[0])
    sorted_entries.reverse()
    return [entry for _date, entry in sorted_entries[:limit]]


@logged
class FeedService(BaseService):
    """
    Import/Update feeds.

    :keyword post_limit: See :attr`post_limit`.
    :keyword update_on_import: See :attr:`update_on_import`.
    :keyword logger: See :attr:`logger`.
    :keyword timeout: See :attr:`timeout`.

    .. attribute:: post_limit

        Default number of posts limit.

    .. attribute:: update_on_import

        By default, fetch new posts when a feed is imported

    .. attribute:: logger

       The :class:`logging.Logger` instance used for logging messages.

    .. attribute:: include_categories

        By default, include feed/post categories.

    .. attribute:: include_enclosures

        By default, include post enclosures.

    .. attribute:: timeout

        Default feed timeout.

    .. attribute:: parser

        The feed parser used. (Default: :mod:`feedparser`.)
    """
    post_field_handlers = {
        "content": find_post_content,
        "published": date_to_datetime("published_parsed"),
        "updated": date_to_datetime("published_parsed"),
        "link": lambda feed_obj, entry: entry.get("link") or feed_obj.feed_url,
        "feed": lambda feed_obj, entry: feed_obj,
        "guid": get_entry_guid,
        "title": lambda feed_obj, entry: entry.get("title", "(no title)").strip(),
        "author": lambda feed_obj, entry: entry.get("author", "").strip(),
    }

    def __init__(self, **kwargs):
        self.post_limit = kwargs.get("post_limit", settings.MAILME_POST_LIMIT)
        self.update_on_import = kwargs.get("update_on_import", True)
        self.include_categories = kwargs.get("include_categories", True)
        self.include_enclosures = kwargs.get("include_enclosures", True)
        self.timeout = kwargs.get("timeout", settings.MAILME_FEED_TIMEOUT)

    def parse_feed(self, feed_url, etag=None, modified=None, timeout=None,
                   maxlen=None):
        """
        Parse feed using feedparser.

        :param feed_url: URL to the feed to parse.

        :keyword etag: E-tag recevied from last parse (if any).
        :keyword modified: ``Last-Modified`` HTTP header received from last
            parse (if any).
        :keyword timeout: Parser timeout in seconds.
        """
        self.logger.debug('parsing feed {}'.format(feed_url))
        prev_timeout = socket.getdefaulttimeout()
        timeout = timeout or self.timeout
        socket.setdefaulttimeout(timeout)

        try:
            if maxlen:
                headers = requests.head(feed_url).headers
                contentlen = int(headers.get("content-length") or 0)
                if contentlen > maxlen:
                    raise exceptions.FeedCriticalError(FEED_GENERIC_ERROR_TEXT)

            feed = feedparser.parse(feed_url,
                                    etag=etag,
                                    modified=modified)

        finally:
            socket.setdefaulttimeout(prev_timeout)

        return feed

    def handle(self, feed_url, **kwargs):
        """
        Import feed.

        If feed is not seen before it will be created, otherwise
        just updated.

        :param feed_url: URL to the feed to import.
        :keyword force: Force import of feed even if it's been updated
            recently.
        """
        self.logger.debug('import feed {}'.format(feed_url))
        force = kwargs.pop('force', None)
        local = kwargs.pop('local', False)
        feed_url = feed_url.strip()
        feed = None
        try:
            feed_obj = Feed.objects.get(feed_url=feed_url)
        except Feed.DoesNotExist:
            try:
                feed = self.parse_feed(feed_url)
            except socket.timeout:
                Feed.objects.create(feed_url=feed_url)
                raise exceptions.TimeoutError(FEED_TIMEDOUT_ERROR_TEXT)
            except Exception:
                feed = {"status": 500}

            default_status = codes.NOT_FOUND
            if local:
                default_status = codes.OK

            status = feed.get("status", default_status)
            if status == codes.NOT_FOUND:
                raise exceptions.FeedNotFoundError(str(FEED_NOT_FOUND_ERROR_TEXT), feed_url)
            if status not in ACCEPTED_STATUSES:
                raise exceptions.FeedCriticalError(
                    FEED_GENERIC_ERROR_TEXT,
                    status=status)

            # Feed can be local/fetched with a HTTP client.
            status = feed.get("status") or feed.get("status\n") or codes.OK

            if status == codes.FOUND or status == codes.MOVED_PERMANENTLY:
                if feed_url != feed.href:
                    return self.handle(feed.href, force=force)

            feed_title = feed.channel.get("title", "(no title)").strip()

            feed_obj = Feed.objects.update_or_create(feed_url=feed_url, **{
                'title': feed_title,
                'description': feed.channel.get('description', '')
            })

            if self.include_categories:
                feed_obj.categories.add(*self.get_categories(feed.channel))

        if self.update_on_import:
            feed_obj = self.update(feed_obj, feed=feed, force=force)

        return feed_obj

    def update(self, feed_obj, **kwargs):
        """
        Update (refresh) feed.

        The feed must already exist in the system, if not you have
        to import it using :meth:`import_feed`.

        :param feed_obj: the Feed object
        :keyword feed: If feed has already been parsed you can pass the
            structure returned by the parser so it doesn't have to be parsed
            twice.
        :keyword force: Force refresh of the feed even if it has been
            recently refreshed already.
        """
        feed = kwargs.pop('feed', None)
        force = kwargs.pop('force', False)
        now = datetime.utcnow().replace(tzinfo=utc)
        already_fresh = (feed_obj.date_last_refresh and
                         now < feed_obj.date_last_refresh +
                         settings.MAILME_MIN_REFRESH_INTERVAL)

        if already_fresh and not force:
            self.logger.info(
                "Feed %s is fresh. Skipping refresh." % feed_obj.feed_url)
            return feed_obj

        limit = self.post_limit
        if not feed:
            last_modified = None
            if feed_obj.http_last_modified and not force:
                last_modified = feed_obj.http_last_modified.timetuple()
            etag = feed_obj.http_etag if not force else None

            try:
                feed = self.parse_feed(feed_obj.feed_url,
                                       etag=etag,
                                       modified=last_modified)
            except socket.timeout:
                return feed_obj.save_timeout_error()
            except Exception:
                return feed_obj.save_generic_error()

        # Feed can be local/ not fetched with HTTP client.
        status = feed.get("status", codes.OK)
        if status == codes.NOT_MODIFIED and not force:
            return feed_obj

        if feed_obj.is_error_status(status):
            return feed_obj.set_error_status(status)

        if feed.entries:
            sorted_by_date = entries_by_date(feed.entries, limit)
            for entry in sorted_by_date:
                self.import_entry(entry, feed_obj)

        feed_obj.date_last_refresh = now
        feed_obj.http_etag = feed.get("etag", "")
        if hasattr(feed, "modified") and feed.modified:
            try:
                timestamp = time.mktime(feed.modified)
                modified = datetime.fromtimestamp(timestamp).replace(tzinfo=utc)
                feed_obj.http_last_modified = modified
            except TypeError:
                pass

        self.logger.debug(
            "Saving feed object... %s" % (feed_obj.feed_url)
        )

        feed_obj.save()
        return feed_obj

    def import_opml(self, feed_url):
        feed = self.parse_feed(feed_url)
        success = []
        errors = []
        if 'opml' in feed['feed']:
            opml = listparser.parse(feed_url)
            for item in opml['feeds']:
                try:
                    feed = self.handle(item['url'])
                    success.append(feed)
                except (exceptions.FeedCriticalError, exceptions.TimeoutError) as exc:
                    errors.append((feed_url, exc))
        else:
            try:
                feed = self.handle(feed_url)
                success.append(feed)
            except (exceptions.FeedCriticalError, exceptions.TimeoutError) as exc:
                errors.append((feed_url, exc))
        return success, errors

    def get_categories(self, obj):
        """Get and save categories."""
        categories = []
        for category in getattr(obj, 'categories', []):
            categories.append(self.create_category(*category))
        return categories

    def create_category(self, domain, title):
        """
        Create new category.

        :param domain: The category domain.
        :param title: The title of the category.
        """
        return Category.objects.update_or_create(
            title=title.strip(),
            domain=domain and domain.strip() or ""
        )

    def create_enclosure(self, **kwargs):
        """Create new enclosure."""
        kwargs.setdefault("length", 0)
        return Enclosure.objects.update_or_create(**kwargs)

    def get_enclosures(self, entry):
        """Get and create enclosures for feed."""
        enclosures = []
        for enclosure in getattr(entry, 'enclosures', []):
            href = getattr(enclosure, 'href', None)
            type = getattr(enclosure, 'type', None)
            if href is None or type is None:
                # Example feed with fully empty enclosures: http://blog.xfce.org/feed/
                continue

            if enclosure and hasattr(enclosure, 'length'):
                try:
                    # Some feeds an empty length instead of an explicit 0
                    # to determine that they are not capable of determining
                    # the lengh.
                    # Spec: When an enclosure's size cannot be determined,
                    #       a publisher should use a length of 0.
                    length = int(enclosure.length)
                except ValueError:
                    length = 0

                enclosures.append(self.create_enclosure(
                    url=enclosure.href,
                    length=length,
                    type=enclosure.type
                ))

        return enclosures

    def post_fields_parsed(self, entry, feed_obj):
        """Parse post fields."""
        return dict(
            (key, handler(feed_obj, entry))
            for key, handler in list(self.post_field_handlers.items())
        )

    def import_entry(self, entry, feed_obj):
        """Import feed post entry."""
        self.logger.debug("Importing entry... %s" % feed_obj.feed_url)

        fields = self.post_fields_parsed(entry, feed_obj)
        post = Post.objects.update_or_create(feed_obj, **fields)

        if self.include_enclosures:
            post.enclosures.add(*(self.get_enclosures(entry) or []))
        if self.include_categories:
            post.categories.add(*(self.get_categories(entry) or []))

        self.logger.debug("Post successfully imported... %s" % (
            feed_obj.feed_url))

        return post
