from django.conf.urls import url, patterns


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
