# -*- coding: utf-8 -*-
import os
import time
import socket
import tempfile
import pytz
from requests import codes
from datetime import datetime
from django.test import TestCase

from mailme.collector.backends.feed import FeedCollector
from mailme.core.exceptions import FeedCriticalError, TimeoutError, FeedNotFoundError
from mailme.core.models import (
    Feed,
    FEED_NOT_FOUND_ERROR,
    FEED_GENERIC_ERROR,
    FEED_TIMEDOUT_ERROR
)

data_path = os.path.join(os.path.dirname(__file__), "data")

FEED_YIELDING_404 = "http://de.yahoo.com/rssmhwqgiuyeqwgeqygqfyf"


def get_data_filename(name):
    return os.sep.join([data_path, name])


def get_data_file(name, mode="r"):
    with open(get_data_filename(name), mode) as file:
        return file.read()


class TestFeedDuplication(TestCase):

    def setUp(self):
        self.collector = FeedCollector()
        self.feeds = list(map(get_data_filename,
            ["t%d.xml" % i for i in reversed(list(range(1, 6)))]))

    def assertImportFeed(self, filename, name):
        feed_obj = self.collector.handle(filename, local=True, force=True)
        self.assertEqual(feed_obj.title, name)
        return feed_obj

    def test_does_not_duplicate_posts(self):
        spool = tempfile.mktemp(suffix="ut", prefix="mailme")

        def test_file(filename):
            try:
                with open(filename) as r:
                    with open(spool, "w") as w:
                        w.write(r.read())
                return self.assertImportFeed(spool,
                    "Saturday Morning Breakfast Cereal (updated daily)")
            finally:
                os.unlink(spool)

        for i in range(40):
            for filename in self.feeds:
                f = test_file(filename)

        posts = list(f.get_posts())
        self.assertEqual(len(posts), 4)

        seen = set()
        for post in posts:
            self.assertNotIn(post.title, seen)
            seen.add(post.title)

        self.assertEqual(posts[0].title, "November 23, 2009")
        self.assertEqual(posts[1].title, "November 22, 2009")
        self.assertEqual(posts[2].title, "November 21, 2009")
        self.assertEqual(posts[3].title, "November 20, 2009")


class TestFeedCollector(TestCase):

    def setUp(self):
        self.feed = get_data_filename("example_feed.rss")
        self.empty_feed = get_data_filename("example_empty_feed.rss")
        self.feed_content_encoded = get_data_filename(
            "example_feed-content_encoded.rss")
        self.collector = FeedCollector()

    def test_import_empty_feed(self):
        feed = self.empty_feed
        collector = self.collector
        feed_obj = collector.handle(feed, local=True)
        self.assertEqual(feed_obj.title, "(no title)")
        self.assertEqual(feed_obj.get_post_count(), 0, "feed has 0 items")
        self.assertEqual(feed_obj.feed_url, feed, "feed url is filename")

    def test_handle(self):
        feed = self.feed
        collector = self.collector
        feed_obj = collector.handle(feed, local=True)
        self.assertEqual(feed_obj.title, "Lifehacker", "feed title is set")
        self.assertEqual(feed_obj.get_post_count(), 20, "feed has 20 items")
        self.assertEqual(feed_obj.feed_url, feed, "feed url is filename")
        self.assertTrue(feed_obj.description, "feed has description")

        posts = feed_obj.get_posts()
        first_post = posts[0]
        self.assertEqual(first_post.guid, "Lifehacker-5147831")
        self.assertEqual(first_post.updated,
                         datetime(2009, 2, 6, 4, 30, 0, 0,
                                  tzinfo=pytz.timezone('US/Pacific')).astimezone(
                             pytz.utc))

        for post in posts:
            self.assertTrue(post.guid, "post has GUID")
            self.assertTrue(post.title, "post has title")
            if hasattr(post, "enclosures"):
                self.assertEqual(post.enclosures.count(), 0,
                                 "post has no enclosures")
            self.assertTrue(post.link, "post has link")
            self.assertTrue(post.content)

        feed_obj2 = collector.handle(feed)
        self.assertTrue(feed_obj2.date_last_refresh,
                        "Refresh date set")
        self.assertEqual(feed_obj2.id, feed_obj.id,
                         "Importing same feed doesn't create new object")
        self.assertEqual(feed_obj2.get_post_count(), 20,
                         "Re-importing feed doesn't give duplicates")

    def test_404_feed_raises_ok(self):
        collector = self.collector
        with self.assertRaises(FeedNotFoundError):
            collector.handle(FEED_YIELDING_404)

    def test_missing_date_feed(self):
        """Try to reproduce the constant date update bug."""
        feed = get_data_filename("buggy_dates.rss")
        collector = self.collector
        feed_obj = collector.handle(feed, local=True)
        last_post = feed_obj.get_posts()[0]

        feed2 = get_data_filename("buggy_dates.rss")
        feed_obj2 = collector.handle(feed2, local=True)
        last_post2 = feed_obj2.get_posts()[0]

        # if the post is updated, we should see a different datetime
        self.assertEqual(last_post.updated, last_post2.updated)

    def test_missing_date_and_guid_feed(self):
        """Try to reproduce the constant date update bug."""
        feed = get_data_filename("buggy_dates_and_guid.rss")
        collector = self.collector
        feed_obj = collector.handle(feed, local=True)
        last_post = feed_obj.get_posts()[0]

        feed2 = get_data_filename("buggy_dates_and_guid.rss")
        feed_obj2 = collector.handle(feed2, local=True)
        last_post2 = feed_obj2.get_posts()[0]

        # if the post is updated, we should see a different datetime
        self.assertEqual(last_post.updated, last_post2.updated)

    def test_socket_timeout(self):

        class _TimeoutFeedCollector(FeedCollector):

            def parse_feed(self, *args, **kwargs):
                raise socket.timeout(.1)

        feed2 = "foofoobar.rss"
        with self.assertRaises(TimeoutError):
            _TimeoutFeedCollector().handle(feed2, local=True)
        self.assertTrue(Feed.objects.get(feed_url=feed2))

    def test_update_feed_socket_timeout(self):

        class _TimeoutFeedCollector(FeedCollector):

            def parse_feed(self, *args, **kwargs):
                raise socket.timeout(.1)

        collector = FeedCollector(update_on_import=False)
        feed_obj = collector.handle(self.feed, local=True, force=True)

        scollector = _TimeoutFeedCollector()
        feed_obj = scollector.update(feed_obj=feed_obj, force=True)
        self.assertEqual(feed_obj.last_error, FEED_TIMEDOUT_ERROR)

    def test_update_feed_parse_feed_raises(self):

        class _RaisingFeedCollector(FeedCollector):

            def parse_feed(self, *args, **kwargs):
                raise KeyError("foo")

        collector = FeedCollector(update_on_import=False)
        feed_obj = collector.handle(self.feed, local=True, force=True)

        scollector = _RaisingFeedCollector()
        feed_obj = scollector.update(feed_obj=feed_obj, force=True)
        self.assertEqual(feed_obj.last_error, FEED_GENERIC_ERROR)

    def test_update_feed_not_modified(self):

        class _Verify(FeedCollector):

            def parse_feed(self, *args, **kwargs):
                feed = super(_Verify, self).parse_feed(*args, **kwargs)
                feed["status"] = codes.NOT_MODIFIED
                return feed

        collector = FeedCollector(update_on_import=False)
        feed_obj = collector.handle(self.feed, local=True, force=True)
        self.assertTrue(_Verify().update(feed_obj=feed_obj, force=False))

    def test_update_feed_error_status(self):

        class _Verify(FeedCollector):

            def parse_feed(self, *args, **kwargs):
                return {"status": codes.NOT_FOUND}

        collector = FeedCollector(update_on_import=False)
        feed_obj = collector.handle(self.feed, local=True, force=True)

        feed_obj = _Verify().update(feed_obj=feed_obj, force=True)
        self.assertEqual(feed_obj.last_error, FEED_NOT_FOUND_ERROR)

    def test_parse_feed_raises(self):

        class _RaisingFeedCollector(FeedCollector):

            def parse_feed(self, *args, **kwargs):
                raise KeyError("foo")

        feed2 = "foo1foo2bar3.rss"
        with self.assertRaises(FeedCriticalError):
            _RaisingFeedCollector().handle(feed2, local=True)
        with self.assertRaises(Feed.DoesNotExist):
            Feed.objects.get(feed_url=feed2)

    def test_http_modified(self):
        now = time.localtime()
        now_as_dt = datetime.fromtimestamp(time.mktime(
            now)).replace(tzinfo=pytz.utc)

        class _Verify(FeedCollector):

            def parse_feed(self, *args, **kwargs):
                feed = super(_Verify, self).parse_feed(*args, **kwargs)
                feed.modified = now
                return feed

        i = _Verify()
        feed = i.handle(self.feed, local=True, force=True)
        self.assertEqual(feed.http_last_modified, now_as_dt)

    def test_update_on_import(self):

        class _Verify(FeedCollector):
            updated = False

            def update(self, *args, **kwargs):
                self.updated = True

        imp1 = _Verify(update_on_import=False)
        imp1.handle(self.feed, local=True, force=True)
        self.assertFalse(imp1.updated)

        imp2 = _Verify(update_on_import=True)
        imp1.handle(self.feed, local=True, force=True)
        self.assertFalse(imp2.updated)

    def test_entry_limit(self):
        feed = self.feed
        collector = FeedCollector(post_limit=10)
        feed_obj = collector.handle(feed, local=True)
        self.assertEqual(feed_obj.title, "Lifehacker", "feed title is set")
        self.assertEqual(feed_obj.get_post_count(), 10, "feed has 10 items")

    def test_double_post_bug(self):
        """With some feeds, the posts seem to be imported several times."""
        feed_str = get_data_filename("lefigaro.rss")
        imported_feed = self.collector.handle(feed_str, local=True,
                                                  force=True)
        post_count = imported_feed.post_set.count()
        imported_feed = self.collector.handle(feed_str, local=True,
                                                  force=True)
        self.assertEqual(imported_feed.post_set.count(), post_count,
                         "Posts seems to be imported twice.")
