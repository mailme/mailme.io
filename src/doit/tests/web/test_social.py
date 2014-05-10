import re

import mock
import pytest
from django.contrib.auth import SESSION_KEY
from django.core import mail
from social.apps.django_app.default.models import Code, UserSocialAuth
from social.exceptions import SocialAuthBaseException

from doit.models.user import User
from doit.testutils import get_messages_from_cookie

from doit.tests.factories.user import profile_complete_form_data, UserFactory
from doit.tests.web.fixtures import moves_auth


def test_moves(client, db, google_auth):
    # Step 1: login
    response = client.get('/login/google-oauth2/')
    assert response.status_code == 302
    assert 'accounts.google.com' in response['Location']

    # Step 2: returning from google
    state = re.search(r'state=([^&]+)', response['Location']).group(1)
    data = {
        'redirect_state': state,
        'code': 'test_code',
        'state': state,
    }
    response = client.get('/complete/google-oauth2/', data=data)
    assert response.status_code == 302
    assert response['Location'].endswith('/register/details/')

    # Step 3: complete profile
    profile_data = profile_complete_form_data(email='bar@none.none')
    response = client.post('/register/details/', data=profile_data)
    assert response.status_code == 302
    assert response['Location'].endswith('/complete/google-oauth2/')
    assert 'details' in client.session['partial_pipeline']['kwargs']
    assert client.session['partial_pipeline']['kwargs']['details']['email'] == 'bar@none.none'

    # Step 4: complete
    response = client.get('/complete/google-oauth2/')
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'

    # We did send out an email validation mail
    assert Code.objects.all().count() == 1
    assert len(mail.outbox) == 1
    assert len(get_messages_from_cookie(response.cookies)) == 1

    user = User.objects.get(social_auth__uid='foo@bar.com')
    assert user.is_active
    assert not user.email_verified

    # Step 5: Complete email validation
    code = Code.objects.all().get()
    response = client.get('/register/confirm_email/%s/' % code.code)
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'

    # Check data
    user = User.objects.get(social_auth__uid='foo@bar.com')
    assert user.is_active
    assert user.email_verified
    assert user.social_auth.get(provider='google-oauth2')
    assert SESSION_KEY in client.session
