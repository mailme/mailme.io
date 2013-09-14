from django.contrib import admin
from django.conf.urls import url, include, patterns

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mailme.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
