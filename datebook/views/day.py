# -*- coding: utf-8 -*-
"""
Page document views
"""
import datetime

from django.conf import settings
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from datebook.models import DayEntry
from datebook.mixins import DatebookCalendarMixin
from datebook.forms.day import DayEntryForm
from datebook.utils import week_from_date

class DayEntryBaseFormView(DatebookCalendarMixin):
    """
    DayEntry base form view
    """
    model = DayEntry
    context_object_name = "dayentry"
    template_name = "datebook/datebook_day_form.html"
    form_class = DayEntryForm

    def get_form(self, form_class):
        """
        Add required args to form instance
        """
        return form_class(self.datebook, self.day, **self.get_form_kwargs())
    
    def get(self, request, *args, **kwargs):
        self.datebook = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        
        return super(DayEntryBaseFormView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.datebook = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        
        return super(DayEntryBaseFormView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('datebook-author-month-week', kwargs={
            'author': self.author,
            'year': self.object.activity_date.year,
            'month': self.object.activity_date.month,
            'week': week_from_date(self.object.activity_date),
        })


class DayEntryFormCreateView(DayEntryBaseFormView, generic.CreateView):
    """
    DayEntry form create view
    """
    def get_form_kwargs(self):
        """
        Put the initial data for the datetime start and stop
        
        TODO: Time start and stop should comes from the User profile settings (date 
              allways come from the datebook period and the required day).
        """
        kwargs = super(DayEntryFormCreateView, self).get_form_kwargs()
        day_date = self.datebook.period.replace(day=self.day)
        time_start = datetime.time(9, 0)
        time_stop = datetime.time(18, 0)
        kwargs.update({
            'initial': {
                'start' : datetime.datetime.combine(day_date, time_start),
                'stop' : datetime.datetime.combine(day_date, time_stop),
                'pause' : datetime.time(1, 0),
            }
        })
        return kwargs


class DayEntryFormEditView(DayEntryBaseFormView, generic.UpdateView):
    """
    DayEntry form edit view
    """
    def get_object(self):
        """
        Add required args to form instance
        """
        return self.datebook.dayentry_set.get(activity_date__day=self.day)
