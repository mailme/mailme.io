from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include, patterns
from django.conf.urls.static import static


urlpatterns = patterns('mailme.web.views',
    url(r'^$', 'home',
        name='home'),
    url(r'^login/$', 'home',
        name='login'),
    url(r'^account/$', 'account',
        name='account'),
    url(r'^logout/$', 'logout',
        name='logout'),
    url(r'^login-redirect/$', 'login_redirect',
        name='redirect'),
)
