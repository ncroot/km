# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.urls import urlpatterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .starter.views import HomePageView
from settings import PROJECT_NAME


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('%s.starter.urls' % PROJECT_NAME)),
    url(r'^core/', include('%s.core.urls' % PROJECT_NAME)),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
