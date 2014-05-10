from django.contrib import admin
from django.conf.urls import url, include, patterns
from mailme.web import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(),
        name='mailme-index'),

    # Account
    url(r'^register/$', views.RegisterView.as_view(),
        name='mailme-register'),
    url(r'^register/details/$', views.UserDetailsView.as_view(),
        name='mailme-register-userdetails'),
    url(r'^register/confirm_email/(?P<code>\w{32})/$',
        views.EmailVerificationView.as_view(),
        name='mailme-email-verification'),
    url(r'^logout/$', views.LogoutView.as_view(),
        name='mailme-logout'),
    url(r'^login/$', views.LoginView.as_view(),
        name='mailme-login'),

    # Social auth
    url(r'', include('social.apps.django_app.urls', namespace='social')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

)
