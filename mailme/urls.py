from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include, patterns
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'mailme.web.views.index', name='web-index'),

)


# Only for development during DEBUG.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
