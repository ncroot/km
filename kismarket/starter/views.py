# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'HomePage.html'
    def get_context_data(self, **kwargs):
        cd = super(HomePageView, self).get_context_data(**kwargs)
        return cd