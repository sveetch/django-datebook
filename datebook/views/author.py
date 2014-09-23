# -*- coding: utf-8 -*-
"""
Datebook author views
"""
import datetime

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
    
    Display all years that have one or more Datebooks for the given user
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

    def get_form(self, form_class):
        if not self.request.user.is_superuser and self.request.user != self.author and not self.request.user.has_perm('datebook.add_datebook'):
            return None
        return super(DatebookAuthorView, self).get_form(form_class)
        
    def get_form_kwargs(self, **kwargs):
        kwargs = super(DatebookAuthorView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'author': self.author,
            'queryset': self.queryset,
        })
        return kwargs
        
    def format_year_list(self, queryset):
        """
        Reformate the paginated queryset to replace items with a tuple containing the 
        item's year, datetime and it's opened month counter
        """
        return [(item.year, item, self.count_opened_months(item.year)) for item in queryset]
        
    def count_opened_months(self, year):
        return Datebook.objects.filter(author=self.author, period__year=year).count()
        
    def get_context_data(self, **kwargs):
        context = super(DatebookAuthorView, self).get_context_data(**kwargs)
        context.update({
            'author': self.author,
            'today': datetime.datetime.today(),
            'object_list': self.format_year_list(context['object_list']),
        })
        return context

    def get_success_url(self):
        return reverse('datebook:year-detail', kwargs={
            'author': self.author,
            'year': self.object.period.year,
        })
