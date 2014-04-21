# -*- coding: utf-8 -*-
"""
    mailme.services.base
    ~~~~~~~~~~~~~~~~~~~~

    Base implementation for every service.
"""


class BaseService(object):
    """Base class for implementing services."""

    name = None

    def handle(self, identifier, **kwargs):
        """Handle **identifier**. Collect sources, update the database."""
        return None

    def update(self, obj, **kwargs):
        """Update (refresh) a source.

        **obj** must already exist in the database, if not you have
        to import it initially using :meth:`collect`.
        """
        return None
