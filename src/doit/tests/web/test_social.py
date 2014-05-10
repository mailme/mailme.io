import re

import mock
import pytest
from django.contrib.auth import SESSION_KEY
from django.core import mail
from social.apps.django_app.default.models import Code, UserSocialAuth
from social.exceptions import SocialAuthBaseException

from doit.models.user import User
from doit.testutils import get_messages_from_cookie

from doit.tests.factories.user import UserFactory
from doit.tests.web.fixtures import moves_auth


def test_moves(client, db, moves_auth):
    # Step 1: login
    response = client.get('/login/moves-oauth2/')
    assert response.status_code == 302
    assert 'api.moves-app.com' in response['Location']

    # Step 2: returning from google
    state = re.search(r'state=([^&]+)', response['Location']).group(1)
    data = {
        'redirect_state': state,
        'code': 'test_code',
        'state': state,
    }
    response = client.get('/complete/moves-oauth2/', data=data)
    assert response.status_code == 302
    assert response['Location'].endswith('/complete/moves-oauth2/')

    # Step 3: complete
    response = client.get('/complete/moves-oauth2/')
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'

    # We did send out an email validation mail
    assert Code.objects.all().count() == 1
    assert len(mail.outbox) == 1
    assert len(get_messages_from_cookie(response.cookies)) == 1

    user = User.objects.get(social_auth__uid='10101010101')
    assert user.is_active
    assert not user.email_verified

    # Check data
    user = User.objects.get(social_auth__uid='101010101001')
    assert user.is_active
    assert user.social_auth.get(provider='moves-oauth2')
    assert SESSION_KEY in client.session
