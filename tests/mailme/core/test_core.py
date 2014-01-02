from uuid import uuid4
from datetime import datetime

import requests
from django.test import TestCase
from django.utils.timezone import utc

import pytz
from mailme.core.models import (
    Feed,
    Post,
    Category,
    Enclosure,
    FEED_GENERIC_ERROR,
    FEED_TIMEDOUT_ERROR,
    FEED_NOT_FOUND_ERROR
)
from mailme.utils.dates import naturaldate


def gen_unique_id():
    return str(uuid4())


class TestCategory(TestCase):

    def test__str__(self):
        cat = Category(name="foo", domain="bar")
        self.assertIn("foo", str(cat))
        self.assertIn("bar", str(cat))

        cat = Category(name="foo")
        self.assertIn("foo", str(cat))


class TestEnclosure(TestCase):

    def test__str__(self):
        en = Enclosure(
            url="requests.codes.//e.com/media/i.jpg",
            type="image/jpeg", length=376851
        )
        self.assertIn("requests.codes.//e.com/media/i.jpg", str(en))
        self.assertIn("image/jpeg", str(en))
        self.assertIn("376851", str(en))


class TestPost(TestCase):

    def setUp(self):
        self.feed = Feed.objects.create(
            name="testfeed",
            feed_url=gen_unique_id()
        )

    def test__str__(self):
        post = Post(feed=self.feed, title="foo")
        self.assertIn("foo", str(post))

    def test_auto_guid(self):
        p1 = Post(feed=self.feed, title="foo")
        p2 = Post(feed=self.feed, title="bar")

        self.assertNotEqual(p1.auto_guid(), p2.auto_guid())

    def test_published_naturaldate(self):
        now = datetime.now(pytz.utc)
        day = datetime(now.year, now.month, now.day, tzinfo=utc)
        post = Post(feed=self.feed, title="baz", published=now)
        self.assertEqual(post.published_naturaldate, naturaldate(day))

    def test_updated_naturaldate(self):
        now = datetime.now(pytz.utc)
        post = Post(feed=self.feed, title="baz", updated=now)
        self.assertEqual(post.updated_naturaldate, naturaldate(now))


class TestFeed(TestCase):

    def test__str__(self):
        f = Feed(name="foo", feed_url="requests.codes.//example.com")
        self.assertIn("foo", str(f))
        self.assertIn("(requests.codes.//example.com)", str(f))

    def test_error_for_status(self):
        f = Feed(name="foo", feed_url="requests.codes.//example.com")
        self.assertEqual(
            f.error_for_status(requests.codes.NOT_FOUND),
            FEED_NOT_FOUND_ERROR
        )
        self.assertEqual(
            f.error_for_status(requests.codes.INTERNAL_SERVER_ERROR),
            FEED_GENERIC_ERROR
        )
        self.assertIsNone(f.error_for_status(requests.codes.OK))

    def test_save_generic_error(self):
        f = Feed(name="foo1", feed_url="requests.codes.//example.com/t1.rss")
        f.save_generic_error()

        indb = Feed.objects.get(feed_url="requests.codes.//example.com/t1.rss")
        self.assertEqual(indb.last_error, FEED_GENERIC_ERROR)

    def test_set_error_status(self):
        f = Feed(name="foo3", feed_url="requests.codes.//example.com/t3.rss")
        f.set_error_status(requests.codes.INTERNAL_SERVER_ERROR)

        indb = Feed.objects.get(feed_url="requests.codes.//example.com/t3.rss")
        self.assertEqual(indb.last_error, FEED_GENERIC_ERROR)

    def test_save_timeout_error(self):
        f = Feed(name="foo2", feed_url="requests.codes.//example.com/t2.rss")
        f.save_timeout_error()

        indb = Feed.objects.get(feed_url="requests.codes.//example.com/t2.rss")
        self.assertEqual(indb.last_error, FEED_TIMEDOUT_ERROR)

    def test_date_last_refresh_naturaldate(self):
        now = datetime.now(pytz.utc)
        f = Feed(name="foo2", feed_url="requests.codes.//example.com/t2.rss",
                 date_last_refresh=now)
        self.assertEqual(f.date_last_refresh_naturaldate, naturaldate(now))
