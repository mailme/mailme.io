import json
import re

import httpretty
import pytest

from social.apps.django_app.default.models import DjangoStorage
from social.backends.moves import MovesOAuth2
from social.p3 import urlparse
from social.strategies.django_strategy import DjangoStrategy
from social.utils import parse_qs


def handle_state(backend, start_url, target_url):
    try:
        if backend.STATE_PARAMETER or backend.REDIRECT_STATE:
            query = parse_qs(urlparse(start_url).query)
            target_url = target_url + ('?' in target_url and '&' or '?')
            if 'state' in query or 'redirect_state' in query:
                name = 'state' in query and 'state' or 'redirect_state'
                target_url += '{0}={1}'.format(name, query[name])
    except AttributeError:
        pass
    return target_url


@pytest.yield_fixture
def moves_auth():
    httpretty.enable()

    def callback(method, uri, headers):
        if 'api.moves-app.com/oauth/v1/access_token' in uri:
            body = 'access_token=test_access_token&token_type=bearer&expires=5156423&user_id=12345'
        else:
            raise Exception('API call without mocking: {0}.'.format(uri))
        return (200, headers, body)

    httpretty.register_uri(httpretty.GET, re.compile(r'.*'), body=callback)

    yield

    httpretty.disable()
    httpretty.reset()


@pytest.yield_fixture
def moves_auth():
    httpretty.enable()

    def _method(method):
        return {'GET': httpretty.GET,
                'POST': httpretty.POST}[method]

    strategy = DjangoStrategy(MovesOAuth2, DjangoStorage)

    start_url = strategy.start().url

    target_url = handle_state(
        MovesOAuth2,
        start_url,
        strategy.build_absolute_uri('/complete/{0}/?code=foobar')
    )

    httpretty.register_uri(
        httpretty.GET,
        start_url,
        status=301,
        location=target_url
    )

    httpretty.register_uri(
        httpretty.GET,
        target_url,
        status=200,
        body='foobar'
    )

    httpretty.register_uri(
        _method(MovesOAuth2.ACCESS_TOKEN_METHOD),
        uri=MovesOAuth2.ACCESS_TOKEN_URL,
        status=200,
        body=json.dumps({
            'access_token': 'foobar',
            'token_type': 'bearer'}),
        content_type='text/json'
    )

    user_data_url = 'https://api.moves-app.com.com/oauth2/v1/user/profile'

    if user_data_url:
        httpretty.register_uri(
            httpretty.GET,
            user_data_url,
            body=json.dumps({'userId': '1010101010011'}),
            content_type='application/json'
        )

    yield

    httpretty.disable()
    httpretty.reset()
