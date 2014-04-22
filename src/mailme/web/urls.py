from django.conf.urls import url, patterns

from mailme.web import views


urlpatterns = patterns('mailme.web.views',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^register/details/$', views.UserDetailsView.as_view(),
        name='register_userdetails'),
    url(r'^register/confirm_email/(?P<code>\w{32})/$',
        views.EmailVerificationView.as_view(),
        name='email_verification'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
)
