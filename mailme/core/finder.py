#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pkg_resources
import logging
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def coerce_url(url):
    url = url.strip()
    if url.startswith("feed://"):
        return "http://{0}".format(url[7:])
    for proto in ["http://", "https://"]:
        if url.startswith(proto):
            return url
    return "http://{0}".format(url)


class FeedFinder(object):

    def __init__(self, user_agent=None):
        if user_agent is None:
            user_agent = "MailMe/{0}".format(
                pkg_resources.get_distribution('mailme').version or 'unknown'
            )
        self.user_agent = user_agent

    def get_feed(self, url):
        try:
            r = requests.get(url, headers={"User-Agent": self.user_agent})
        except Exception as e:
            logging.warn("Error while getting '{0}'".format(url))
            logging.warn("{0}".format(e))
            return None
        return r.text

    def is_feed_data(self, text):
        data = text.lower()
        if data.count("<html"):
            return False
        return data.count("<rss")+data.count("<rdf")+data.count("<feed")

    def is_feed(self, url):
        text = self.get_feed(url)
        if text is None:
            return False
        return self.is_feed_data(text)

    def is_feed_url(self, url):
        return any(map(url.lower().endswith,
                       [".rss", ".rdf", ".xml", ".atom"]))

    def is_feedlike_url(self, url):
        return any(map(url.lower().count,
                       ["rss", "rdf", "xml", "atom", "feed"]))


def find_feeds(url, check_all=False, user_agent=None):
    finder = FeedFinder(user_agent=user_agent)

    # Format the URL properly.
    url = coerce_url(url)

    # Download the requested URL.
    text = finder.get_feed(url)
    if text is None:
        return []

    # Check if it is already a feed.
    if finder.is_feed_data(text):
        return [url]

    # Look for <link> tags.
    logging.info("Looking for <link> tags.")
    tree = BeautifulSoup(text)
    links = []
    for link in tree.find_all("link"):
        if link.get("type") in ["application/rss+xml",
                                "text/xml",
                                "application/atom+xml",
                                "application/x.atom+xml",
                                "application/x-atom+xml"]:
            links.append(urljoin(url, link.get("href", "")))

    # Check the detected links.
    urls = [link for link in links if finder.is_feed(link)]
    logging.info("Found {0} feed <link> tags.".format(len(urls)))
    if len(urls) and not check_all:
        return sort_urls(urls)

    # Look for <a> tags.
    logging.info("Looking for <a> tags.")
    local, remote = [], []
    for a in tree.find_all("a"):
        href = a.get("href", None)
        if href is None:
            continue
        if "://" not in href and finder.is_feed_url(href):
            local.append(href)
        if finder.is_feedlike_url(href):
            remote.append(href)

    # Check the local URLs.
    local = [urljoin(url, l) for l in local]
    urls += [link for link in local if finder.is_feed(link)]
    logging.info("Found {0} local <a> links to feeds.".format(len(urls)))
    if len(urls) and not check_all:
        return sort_urls(urls)

    # Check the remote URLs.
    remote = [urljoin(url, l) for l in remote]
    urls += [link for link in remote if finder.is_feed(link)]
    logging.info("Found {0} remote <a> links to feeds.".format(len(urls)))
    if len(urls) and not check_all:
        return sort_urls(urls)

    # Guessing potential URLs.
    fns = ["atom.xml", "index.atom", "index.rdf", "rss.xml", "index.xml",
           "index.rss"]
    urls += [link for link in [urljoin(url, f) for f in fns]
                  if finder.is_feed(link)]
    return sort_urls(urls)


def url_feed_prob(url):
    if "comments" in url:
        return -1
    kw = ["atom", "rss", "rdf", ".xml", "feed"]
    for p, t in zip(range(len(kw), 0, -1), kw):
        return p
    return 0


def sort_urls(feeds):
    return sorted(list(set(feeds)), key=url_feed_prob, reverse=True)


if __name__ == "__main__":
    print(find_feeds("www.preposterousuniverse.com/blog/"))
    print(find_feeds("http://xkcd.com"))
    print(find_feeds("dan.iel.fm/atom.xml"))
    print(find_feeds("dan.iel.fm", check_all=True))
    print(find_feeds("kapadia.github.io"))
    print(find_feeds("blog.jonathansick.ca"))
    print(find_feeds("asdasd"))
