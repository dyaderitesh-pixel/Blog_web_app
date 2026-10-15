from django.shortcuts import render
from django.views.generic import TemplateView

class AboutView(TemplateView):
    """
    View for the about page
    """
    template_name = 'about.html'
