from django.contrib import auth, messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView
from django.views.generic.edit import FormView

from social.apps.django_app.default.models import Code
from social.apps.django_app.utils import load_strategy
from social.apps.django_app.views import complete

from mailme.core.models import User
from mailme.web.forms import (
    LoginForm,
    RegistrationForm,
    UserDetailsForm,
)


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


class RegisterView(CompleteSocialAuthMixin, FormView):
    form_class = RegistrationForm
    template_name = 'mailme/web/register.html'

    def form_valid(self, form):
        return self.complete(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1'],
        )


class EmailVerificationView(RedirectView):
    permanent = False

    def dispatch(self, request, *args, **kwargs):
        try:
            code = Code.objects.get(code=self.kwargs['code'], verified=False)
            User.objects.get(email__iexact=code.email).verify_email()
            code.verify()
            messages.success(self.request,
                _('Your email address has been verified.'))
        except ObjectDoesNotExist:
            messages.error(self.request,
                _('An error occured while verifying your email address.'))

        return super(EmailVerificationView, self).dispatch(
            request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('web:index')


class LoginView(CompleteSocialAuthMixin, FormView):
    form_class = LoginForm
    template_name = 'mailme/web/login.html'

    def form_valid(self, form):
        return self.complete(details={'user': form.cleaned_data['user']})

    def get_context_data(self, **kwargs):
        data = super(LoginView, self).get_context_data(**kwargs)
        data['login_form'] = data.pop('form')
        return data


class LogoutView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        auth.logout(self.request)
        return reverse('web:index')


class IndexView(LoginView):
    """View for the index page"""
    template_name = 'mailme/web/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        if not self.request.user.is_authenticated():
            return context

        # Do stuff...
        return context


class UserDetailsView(FormView):
    template_name = 'mailme/web/register_userdetails.html'
    form_class = UserDetailsForm

    def form_valid(self, form):
        backend = self.request.session['partial_pipeline']['backend']
        self.request.session['partial_pipeline']['kwargs']['details'].update(
            form.cleaned_data
        )
        self.request.session['require_user_details_valid'] = True
        return redirect('social:complete', backend=backend)

    def get_initial(self):
        return self.request.session['partial_pipeline']['kwargs']['details']
