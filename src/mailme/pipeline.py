from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from social.exceptions import AuthException
from social.pipeline.partial import partial
from social.pipeline.social_auth import social_details


SKIP_UNIQUE_LOGIN = ('username',)


class UniqueLoginException(AuthException):
    def __str__(self):
        return 'User is already logged in.'


def unique_login(strategy, user=None, *args, **kwars):
    if user and strategy.backend.name not in SKIP_UNIQUE_LOGIN:
        raise UniqueLoginException(strategy.backend)


def conditional_social_details(strategy, response, *args, **kwargs):
    # Override default social_details if we already have a user.
    # We do this, to ensure the username from db is used and not the entered
    # one. (would raise errors on usersocialauth objects)
    has_user_data = kwargs.get('details', {}).get('user', None) is not None

    if strategy.backend.name == 'username' and has_user_data:
        return {
            'details': {'username': kwargs['details']['user'].username}
        }

    return social_details(strategy, response, *args, **kwargs)


@partial
def require_user_details(strategy, details, user=None, is_new=False, *args, **kwargs):
    required_fields = settings.SOCIAL_AUTH_REQUIRED_USER_FIELDS

    skip = strategy.backend.name == 'username'

    if user and all(details.get(field, None) for field in required_fields) or skip:
        return
    elif is_new and strategy.session_get('require_user_details_valid', None) is None:
        for key in required_fields:
            if strategy.session_get(key):
                details[key] = strategy.session_pop(key)
        return redirect('mailme-register-userdetails')


def email_verification(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user and is_new is True:
        user.new_email_verification(strategy.request, user.email)
        messages.success(strategy.request, _(
            'We sent you a verification email. Please confirm your email '
            'address by clicking the link in the email.'
        ))
