# -*- coding: utf-8 -*-
"""
    mailme.utils.text
    ~~~~~~~~~~~~~~~~~

    Various text realated tools.
"""
import re

_str_num_re = re.compile(r'(?:[^\d]*(\d+)[^\d]*)+')


def increment_string(s):
    """Increment a number in a string or add a number."""
    m = _str_num_re.search(s)
    if m:
        next = str(int(m.group(1)) + 1)
        start, end = m.span(1)
        if start or end:
            return '{0}-{1}{2}'.format(
                s[:max(end - len(next), start)],
                next,
                s[end:])
    return s + '-2'
