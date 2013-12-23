from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include, patterns
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mailme.web.views.home',
        name='mailme-home'),
    url(r'^login/$', 'mailme.web.views.home',
        name='mailme-login'),
    url(r'^account/$', 'mailme.web.views.account',
        name='mailme-account'),
    url(r'^login-redirect/$', 'mailme.web.views.login_redirect',
        name='mailme-login-redirect'),
    url(r'^logout/$', 'mailme.web.views.logout',
        name='mailme-logout'),

    url(r'', include('social.apps.django_app.urls',
        namespace='social')),

    url(r'^admin/', include(admin.site.urls)),

)

# Only for development during DEBUG.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
