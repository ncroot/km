# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from models import Branch, Developer, Branch_To_Kis


class BranchAndDeveloperMatrix(TemplateView):
    template_name = '../templates/core/BranchAndDeveloperMatrix.html'
    def get_context_data(self, **kwargs):
        cd = super(BranchAndDeveloperMatrix, self).get_context_data(**kwargs)
        cd.update({
            'branches': Branch.objects.all,
            'developers': Developer.objects.all,
        })
        return cd