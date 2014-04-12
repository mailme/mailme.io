from django.conf.urls import url, patterns

from mailme.web.views import (
    IndexView,
    RegisterView,
    UserDetailsView,
    LogoutView,
    LoginView,
    EmailVerificationView
)


urlpatterns = patterns('mailme.web.views',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^register/details/$', UserDetailsView.as_view(),
        name='register_userdetails'),
    url(r'^register/confirm_email/(?P<code>\w{32})/$',
        EmailVerificationView.as_view(),
        name='email_verification'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^login/$', LoginView.as_view(), name='login'),
)
