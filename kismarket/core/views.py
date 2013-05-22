# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, ListView, DetailView
from kismarket.starter.helper.view import JSONResponseMixinList
from models import Branch, Developer, Customer


class BranchAndDeveloperMatrixView(TemplateView):
    template_name = 'BranchAndDeveloperMatrix.html'
    def get_context_data(self, **kwargs):
        cd = super(BranchAndDeveloperMatrixView, self).get_context_data(**kwargs)
        cd.update({
            'branches': Branch.objects.all,
            'developers': Developer.objects.all,
        })
        return cd


class CustomerListView(TemplateView):
    template_name = 'CustomerListView.html'
    def get_context_data(self, **kwargs):
        cd = super(CustomerListView, self).get_context_data(**kwargs)
        return cd


class CustomerListJSONView(JSONResponseMixinList, ListView):
    def get_queryset(self):
        return Customer.objects.all()
