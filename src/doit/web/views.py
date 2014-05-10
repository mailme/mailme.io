from django.contrib import auth, messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView
from django.views.generic.edit import FormView, TemplateView

from social.apps.django_app.default.models import Code
from social.apps.django_app.utils import load_strategy
from social.apps.django_app.views import complete

from doit.models.user import User


class CompleteSocialAuthMixin(object):
    def complete(self, **kwargs):
        # Before we proceed the auth, clear the session to ensure that no
        # half-backed registrations are left over (this would result in a
        # redirect to extradata after login even if the logged in user has a
        # complete profile.
        self.request.session.clear()

        # Load social strategy to ensure this request looks like a social auth
        # request.
        self.request.social_strategy = load_strategy(backend='username')

        return complete(self.request, 'username', **kwargs)


class LoginView(CompleteSocialAuthMixin, TemplateView):
    template_name = 'doit/web/login.html'


class LogoutView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        auth.logout(self.request)
        return reverse('doit-index')


class IndexView(LoginView):
    """View for the index page"""
    template_name = 'doit/web/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        if not self.request.user.is_authenticated():
            return context

        # Do stuff...
        return context
