import mock
import pytest
import re

from django.contrib.auth import SESSION_KEY
from django.core import mail
from social.apps.django_app.default.models import Code, UserSocialAuth
from social.exceptions import SocialAuthBaseException

from mailme.core.models import User
from mailme.testutils import get_messages_from_cookie

from mailme.tests.factories.core import profile_complete_form_data, UserFactory
from mailme.tests.web.fixtures import facebook_auth, twitter_auth, google_auth  # noqa


def test_twitter(client, db, twitter_auth):
    # Step 1: login
    response = client.get('/login/twitter/')
    assert response.status_code == 302
    assert 'twitter.com' in response['Location']
    data = {
        'oauth_token': twitter_auth['oauth_token'],
        'oauth_verifier': 'test_oauth_verifier'
    }

    # Step 2: returning from twitter
    response = client.get('/complete/twitter/', data=data)
    assert response.status_code == 302
    assert response['Location'].endswith('/register/details/')

    # Step 3: complete profile
    profile_data = profile_complete_form_data(email='bar@none.none')
    response = client.post('/register/details/', data=profile_data)
    assert response.status_code == 302
    assert response['Location'].endswith('/complete/twitter/')
    assert 'details' in client.session['partial_pipeline']['kwargs']
    assert client.session['partial_pipeline']['kwargs']['details']['email'] == 'bar@none.none'

    # Step 4: complete
    response = client.get('/complete/twitter/')
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'

    # We did send out an email validation mail
    assert Code.objects.all().count() == 1
    assert len(mail.outbox) == 1
    assert len(get_messages_from_cookie(response.cookies)) == 1

    user = User.objects.get(social_auth__uid='12345')
    assert user.is_active
    assert not user.email_verified

    # Step 5: Complete email validation
    code = Code.objects.all().get()
    response = client.get('/register/confirm_email/%s/' % code.code)
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'

    # Check data
    user = User.objects.get(social_auth__uid='12345')
    assert user.is_active
    assert user.email_verified
    assert user.social_auth.get(provider='twitter')
    assert SESSION_KEY in client.session


def test_facebook(client, db, facebook_auth):
    # Step 1: login
    response = client.get('/login/facebook/')
    assert response.status_code == 302
    assert 'facebook.com' in response['Location']

    # Step 2: returning from facebook
    state = re.search(r'state=([^&]+)', response['Location']).group(1)
    data = {
        'redirect_state': state,
        'code': 'test_code',
        'state': state,
    }
    response = client.get('/complete/facebook/', data=data)
    assert response.status_code == 302
    assert response['Location'].endswith('/register/details/')

    # Step 3: complete profile
    profile_data = profile_complete_form_data(email='bar@none.none')
    response = client.post('/register/details/', data=profile_data)
    assert response.status_code == 302
    assert response['Location'].endswith('/complete/facebook/')
    assert 'details' in client.session['partial_pipeline']['kwargs']
    assert client.session['partial_pipeline']['kwargs']['details']['email'] == 'bar@none.none'

    # Step 4: complete
    response = client.get('/complete/facebook/')
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'

    # We did send out an email validation mail
    assert Code.objects.all().count() == 1
    assert len(mail.outbox) == 1
    assert len(get_messages_from_cookie(response.cookies)) == 1

    user = User.objects.get(social_auth__uid='12345')
    assert user.is_active
    assert not user.email_verified

    # Step 5: Complete email validation
    code = Code.objects.all().get()
    response = client.get('/register/confirm_email/%s/' % code.code)
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'

    # Check data
    user = User.objects.get(social_auth__uid='12345')
    assert user.is_active
    assert user.email_verified
    assert user.social_auth.get(provider='facebook')
    assert SESSION_KEY in client.session


def test_google(client, db, google_auth):
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


def test_username_registration(client, db):
    # Step 1: login
    response = client.get('/register/')
    assert response.status_code == 200

    # Step 2: enter all data
    data = {
        'username': 'foo',
        'email': 'foo@bar.com',
        'password1': 'pass12',
        'password2': 'pass12',
    }
    response = client.post('/register/', data=data)
    assert response.status_code == 302

    # For username backend we already have all the information we need
    # in the initial form.
    assert not response['Location'].endswith('/register/details/')

    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'

    # We did send out an email validation mail
    assert Code.objects.all().count() == 1
    assert len(mail.outbox) == 1
    assert len(get_messages_from_cookie(response.cookies)) == 1

    user = User.objects.get(social_auth__uid='foo')
    assert user.is_active
    assert not user.email_verified

    # Step 5: Complete email validation
    code = Code.objects.all().get()
    response = client.get('/register/confirm_email/%s/' % code.code)
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'

    # Check data
    user = User.objects.get(social_auth__uid='foo')
    assert user.is_active
    assert user.email_verified
    assert user.social_auth.get(provider='username')
    assert SESSION_KEY in client.session


def test_username_registration_invalid_email_verification(client, db):
    # Step 1: login
    response = client.get('/register/')
    assert response.status_code == 200

    # Step 2: enter all data
    data = {
        'username': 'foo',
        'email': 'foo@bar.com',
        'password1': 'pass12',
        'password2': 'pass12',
    }
    response = client.post('/register/', data=data)
    assert response.status_code == 302

    # For username backend we already have all the information we need
    # in the initial form.
    assert not response['Location'].endswith('/register/details/')

    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'

    user = User.objects.get(social_auth__uid='foo')
    assert user.is_active
    assert not user.email_verified

    # Step 5: Call invalid email email validation
    response = client.get('/register/confirm_email/%s/' % ('a' * 32))
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'

    # Check data
    user = User.objects.get(social_auth__uid='foo')
    assert not user.email_verified


def test_username_login(client, db):
    # Step 1: login
    response = client.get('/login/')
    assert response.status_code == 200

    user = UserFactory.create(usersocialauth='username')

    # Step 2: enter all data
    data = {
        'username': user.username,
        'password': 'secret',
    }
    response = client.post('/login/', data=data)
    assert response.status_code == 302

    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'

    assert SESSION_KEY in client.session


def test_username_login_uppercase(client, db):
    # Step 1: login
    response = client.get('/login/')
    assert response.status_code == 200

    user = UserFactory.create(usersocialauth='username')

    # Step 2: enter all data
    data = {
        'username': user.username.upper(),
        'password': 'secret',
    }
    response = client.post('/login/', data=data)
    assert response.status_code == 302

    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'

    assert SESSION_KEY in client.session

    assert UserSocialAuth.objects.filter(user=user).count() == 1


def test_username_login_invalid(client, db):
    # Step 1: login
    response = client.get('/login/')
    assert response.status_code == 200

    user = UserFactory.create(usersocialauth='username')

    # Step 2: enter all data
    data = {
        'username': user.username,
        'password': 'secretinvalid',
    }
    response = client.post('/login/', data=data)
    assert response.status_code == 200
    assert response.context_data['login_form'].is_valid() is False

    assert SESSION_KEY not in client.session


@mock.patch('mailme.web.views.complete')
def test_username_handle_unkown_exception(do_complete_mock, client, db):
    do_complete_mock.side_effect = Exception

    # Step 1: login
    response = client.get('/login/')
    assert response.status_code == 200

    user = UserFactory.create(usersocialauth='username')

    # Step 2: enter all data
    data = {
        'username': user.username,
        'password': 'secret',
    }

    with pytest.raises(Exception):
        response = client.post('/login/', data=data)


@mock.patch('mailme.web.views.complete')
def test_username_handle_social_exception(do_complete_mock, client, db):
    do_complete_mock.side_effect = SocialAuthBaseException('test123')

    # Step 1: login
    response = client.get('/login/')
    assert response.status_code == 200

    user = UserFactory.create(usersocialauth='username')

    # Step 2: enter all data
    data = {
        'username': user.username,
        'password': 'secret',
    }

    response = client.post('/login/', data=data)
    assert response.status_code == 302
    assert len(get_messages_from_cookie(response.cookies)) == 1
