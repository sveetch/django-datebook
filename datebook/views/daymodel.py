# -*- coding: utf-8 -*-
"""
Day template views
"""
import datetime

from django.conf import settings
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from braces.views import LoginRequiredMixin

from datebook.models import DayEntry, DayModel
from datebook.views.day import DayEntryFormEditView
from datebook.forms.daymodel import DayToDayModelForm
from datebook.mixins import AuthorKwargsMixin, DatebookCalendarMixin, OwnerOrPermissionRequiredMixin


class DayModelListView(AuthorKwargsMixin, OwnerOrPermissionRequiredMixin, generic.ListView):
    """
    Author's day models index
    """
    model = DayModel
    template_name = "datebook/daymodel/index.html"
    permission_required = 'datebook.change_daymodel'
    paginate_by = None
    
    def get_queryset(self):
        return self.model.objects.filter(author=self.author)


class DayEntryToDayModelFormView(DatebookCalendarMixin, OwnerOrPermissionRequiredMixin, generic.CreateView):
    """
    Form view to create a DayModel object from a DayEntry object
    """
    context_object_name = "dayentry"
    template_name = "datebook/day/form.html"
    form_class = DayToDayModelForm
    permission_required = 'datebook.add_daymodel'
    raise_exception = True

    def get_form(self, form_class):
        """
        Add required args to form instance
        """
        return form_class(self.author, **self.get_form_kwargs())
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, _('Day entry has been created successfully'), fail_silently=True)
        return super(DayEntryToDayModelFormView, self).form_valid(form)
    
    def get_form_kwargs(self):
        """
        Add post form url
        """
        kwargs = super(DayEntryToDayModelFormView, self).get_form_kwargs()
        
        day_date = self.datebook.period.replace(day=self.day)
        time_start = datetime.time(9, 0)
        time_stop = datetime.time(18, 0)
        
        kwargs.update({
            'form_action': '.',
            'dayentry': self.dayentry,
            'day_date': day_date,
            'initial': {
                'start' : self.dayentry.start,
                'stop' : self.dayentry.stop,
                'pause' : self.dayentry.pause,
                'overtime' : self.dayentry.overtime,
                'content' : self.dayentry.content,
            },
        })
        return kwargs


    def get_success_url(self):
        """
        If 'submit_and_next' button has been used, redirect to the next day form, 
        else redirect to the month view
        """
        return reverse('datebook:day-models', kwargs={
            'author': self.author,
        })
    
    def get_dayentry(self):
        """
        Add required args to form instance
        """
        return self.datebook.dayentry_set.get(activity_date__day=self.day)
        
    def get(self, request, *args, **kwargs):
        self.datebook = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        self.author = self.datebook.author
        self.dayentry = self.get_dayentry()
        return super(DayEntryToDayModelFormView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.datebook = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        self.author = self.datebook.author
        self.dayentry = self.get_dayentry()
        return super(DayEntryToDayModelFormView, self).post(request, *args, **kwargs)



class DayModelFormEditView(AuthorKwargsMixin, OwnerOrPermissionRequiredMixin, generic.UpdateView):
    """
    DayModel form edit view
    """
    model = DayModel
    context_object_name = "daymodel"
    template_name = "datebook/day/form.html"
    form_class = DayToDayModelForm
    permission_required = 'datebook.change_daymodel'
    raise_exception = True

    def get_form(self, form_class):
        """
        Add required args to form instance
        """
        return form_class(self.author, **self.get_form_kwargs())
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, _('Day entry has been edited successfully'), fail_silently=True)
        return super(DayModelFormEditView, self).form_valid(form)
    
    def get_form_kwargs(self):
        """
        Add post form url
        """
        kwargs = super(DayModelFormEditView, self).get_form_kwargs()
        
        kwargs.update({
            'form_action': '.',
            'day_date': self.object.start.date(),
        })
        return kwargs
    
    def get_object(self, queryset=None):
        return get_object_or_404(self.model, author=self.author, pk=self.kwargs['pk'])

    def get_success_url(self):
        """
        If 'submit_and_next' button has been used, redirect to the next day form, 
        else redirect to the month view
        """
        return reverse('datebook:day-models', kwargs={
            'author': self.author,
        })

