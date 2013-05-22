# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from .views import BranchAndDeveloperMatrixView, CustomerListView, CustomerListJSONView

urlpatterns = patterns('',
    url(r'^$', BranchAndDeveloperMatrixView.as_view(), name='core-home'),
    url(r'^branch-n-developer$', BranchAndDeveloperMatrixView.as_view(), name='branch-n-developer'),
    url(r'^customer-list$', CustomerListView.as_view(), name='customer-list'),
    url(r'^customer-list-json$', CustomerListJSONView.as_view(), name='customer-list-json'),
)
