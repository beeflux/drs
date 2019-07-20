from django.shortcuts import render
from django.views.generic import TemplateView


class OpenSpaceView(TemplateView):
    def get_context_data(self, ** kwargs):
        data = super(OpenSpaceView, self).get_context_data(**kwargs)
        data['maps'] = []
        return data
    template_name = "openspace/dashboard.html"
