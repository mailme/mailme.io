import factory
from django.contrib.auth.hashers import make_password
from social.apps.django_app.default.models import UserSocialAuth

from mailme.models.user import User


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda i: 'user{0}')
    email = factory.Sequence(lambda i: '{0}@none.none'.format(i))
    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        raw_password = kwargs.pop('raw_password', 'secret')
        if not 'password' in kwargs:
            kwargs['password'] = make_password(raw_password, hasher='md5')
        return super(UserFactory, cls)._prepare(create, **kwargs)

    @factory.post_generation
    def usersocialauth(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            self.social_auth.create(provider=extracted, uid=self.username)


class UserSocialAuthFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UserSocialAuth
    user = factory.SubFactory(UserFactory)
    provider = u'facebook'
    uid = factory.Sequence(lambda i: u'social-{0}'.format(i))


def profile_complete_form_data(optional=False, **kwargs):
    data = {
        'username': 'the foo bar man',
        'email': 'bar@none.none',
    }
    optional = {
    }
    if optional:
        data.update(optional)
    data.update(kwargs)
    return data
