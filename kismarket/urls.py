# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.urls import urlpatterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from kismarket.core.views import BranchAndDeveloperMatrix


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', BranchAndDeveloperMatrix.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
