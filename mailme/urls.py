from django.contrib import admin
from django.conf.urls import url, include, patterns

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       )
