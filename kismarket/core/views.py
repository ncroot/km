# -*- coding: utf-8 -*-
from django.views.generic import TemplateView


class Test(TemplateView):
    template_name = 'templates/test.html'
