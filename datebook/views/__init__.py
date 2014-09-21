# -*- coding: utf-8 -*-
"""
Common views
"""
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from braces.views import LoginRequiredMixin

from datebook.models import Datebook

class IndexView(LoginRequiredMixin, generic.TemplateView):
    """
    Index view
    
    Display all user that have one or more Datebooks
    """
    template_name = "datebook/index.html"
    
    def get(self, request, *args, **kwargs):
        
        context = {
            'object_list': Datebook.objects.filter(author__is_active=True).values('author__username').distinct(),
        }
        
        return self.render_to_response(context)
