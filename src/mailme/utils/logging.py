# -*- coding: utf-8 -*-
import logging
import inspect


def get_logger(obj):
    """Return a logger object with the proper module path for ``obj``."""
    name = None
    module = getattr(inspect.getmodule(obj), '__name__', None)
    if inspect.ismethod(obj):
        name = '{module}.{cls}.{method}'.format(
            module=module,
            cls=type(obj).__name__,
            method=obj.__func__.__name__
        )
    elif inspect.isfunction(obj):
        name = '{module}.{function}'.format(
            module=module,
            function=obj.func_name
        )
    elif inspect.isclass(obj):
        name = '{module}.{cls}'.format(
            module=module,
            cls=obj.__name__
        )
    elif isinstance(obj, (str, bytes)):
        name = obj

    return logging.getLogger(name)


def logged(obj):
    """Decorator to mark a object as logged.

    This injects a ``logger`` instance into ``obj`` to make log statements
    local and correctly named.

    Example:

    .. code:: python

        >>> @logged
        ... class MyClass(object):
        ...     def foo(self):
        ...         self.logger.warning('logged')
        ...
        >>> import logging
        >>> logging.basicConfig()
        >>> obj = MyClass()
        >>> obj.foo()
        WARNING:__main__.MyClass:logged

    Supported objects:

     * Functions
     * Methods
     * Classes
     * Raw names (e.g, user at module level)

    """
    obj.logger = get_logger(obj)
    return obj


def enable_error_logging_in_debug_mode():
    """
    If DEBUG = True then monkey patch the default DEBUG 500 response, so
    that we also log the errors. (So that we can see them retrospectively).
    """
    from django.conf import settings

    if settings.DEBUG:
        from django.views import debug
        import logging

        orig_technical_500_response = debug.technical_500_response

        def custom_technical_500_response(request, exc_type, exc_value, tb):
            """
            Create a technical server error response. The last three arguments are
            the values returned from sys.exc_info() and friends.
            """
            logger = logging.getLogger('django.request')
            logger.error('Internal Server Error: %s' % request.path,
                exc_info=(exc_type, exc_value, tb),
                extra={'status_code': 500, 'request': request}
            )
            return orig_technical_500_response(request, exc_type, exc_value, tb)

        debug.technical_500_response = custom_technical_500_response


# TODO: is there a better init point for this?
enable_error_logging_in_debug_mode()
