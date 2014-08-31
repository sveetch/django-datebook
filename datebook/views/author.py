# -*- coding: utf-8 -*-
"""
Common views
"""
from django.views import generic
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from braces.views import LoginRequiredMixin

from datebook.models import Datebook
from datebook.forms.year import DatebookYearForm
from datebook.utils.views import ListAppendView

class DatebookAuthorView(LoginRequiredMixin, ListAppendView):
    """
    User datebook index
    
    Display all year that have one or more Datebooks for the given user
    """
    model = Datebook
    form_class = DatebookYearForm
    paginate_by = None
    locked_form = False
    template_name = "datebook/author_index.html"
    
    def get_queryset(self, *args, **kwargs):
        self.author = get_object_or_404(User, username=self.kwargs['author'])
        self.queryset = self.model.objects.filter(author=self.author).dates('period', 'year')
        return super(DatebookAuthorView, self).get_queryset(*args, **kwargs)
        
    def get_form_kwargs(self, **kwargs):
        kwargs = super(DatebookAuthorView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'author': self.author,
            'queryset': self.queryset,
        })
        return kwargs
        
    def get_context_data(self, **kwargs):
        context = super(DatebookAuthorView, self).get_context_data(**kwargs)
        context.update({
            'author': self.author,
        })
        return context

    def get_success_url(self):
        return reverse('datebook-author-year', kwargs={
            'author': self.author,
            'year': self.object.period.year,
        })

    #def form_valid(self, form):
        #response = super(DatebookAuthorView, self).get_context_data(**kwargs)
        
        #return response
