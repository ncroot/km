# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from models import Branch, Developer

class BranchAndDeveloperMatrixView(TemplateView):
    template_name = 'BranchAndDeveloperMatrix.html'
    def get_context_data(self, **kwargs):
        cd = super(BranchAndDeveloperMatrixView, self).get_context_data(**kwargs)
        cd.update({
            'branches': Branch.objects.all,
            'developers': Developer.objects.all,
        })
        return cd