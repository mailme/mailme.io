from django.contrib import messages
from django.shortcuts import redirect

from social.apps.django_app import middleware
from social.exceptions import SocialAuthBaseException


class SocialAuthExceptionMiddleware(middleware.SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        self.strategy = getattr(request, 'social_strategy', None)
        if self.strategy is None or self.raise_exception(request, exception):
            return

        if isinstance(exception, SocialAuthBaseException):
            message = self.get_message(request, exception)
            url = self.get_redirect_uri(request, exception)

            messages.error(request, message, self.strategy.backend.name)
            return redirect(url)
