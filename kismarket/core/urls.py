# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from .views import BranchAndDeveloperMatrixView, CustomerListView

urlpatterns = patterns('',
    url(r'^$', BranchAndDeveloperMatrixView.as_view(), name='branch-n-developer'),
    url(r'^branch-n-developer$', BranchAndDeveloperMatrixView.as_view(), name='branch-n-developer'),
    url(r'^customer-list$', CustomerListView.as_view(), name='customer-list'),
)
