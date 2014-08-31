# -*- coding: utf-8 -*-
"""
Common views
"""
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from datebook.models import Datebook

class IndexView(generic.TemplateView):
    """
    Index view
    
    Display all user that have one or more Datebooks
    """
    template_name = "datebook/index.html"
    
    def get(self, request, *args, **kwargs):
        
        context = {
            'object_list': Datebook.objects.all().values('author__username').distinct(),
        }
        
        return self.render_to_response(context)
