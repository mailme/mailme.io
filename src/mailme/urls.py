from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include, patterns
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('mailme.web.urls', namespace='web')),
    url(r'', include('social.apps.django_app.urls',
        namespace='social')),

    url(r'^admin/', include(admin.site.urls)),

)

# Only for development during DEBUG.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
