from django.contrib import admin
from django.conf.urls import url, include, patterns
from doit.web import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(),
        name='doit-index'),

    # Account
    url(r'^register/$', views.RegisterView.as_view(),
        name='doit-register'),
    url(r'^logout/$', views.LogoutView.as_view(),
        name='doit-logout'),
    url(r'^login/$', views.LoginView.as_view(),
        name='doit-login'),

    # Social auth
    url(r'', include('social.apps.django_app.urls', namespace='social')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

)
