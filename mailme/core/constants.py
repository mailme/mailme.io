ACCEPTED_STATUSES = frozenset([http.OK,
                               http.FOUND,
                               http.NOT_MODIFIED,
                               http.MOVED_PERMANENTLY,
                               http.TEMPORARY_REDIRECT])

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
