# -*- coding: utf-8 -*-
"""
View mixins
"""
import datetime

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from datebook.models import Datebook
from datebook.calendars import DatebookCalendar

class AuthorKwargsMixin(object):
    """
    Get the User object for the given "author" kwarg if given
    """
    set_as_attr = True # IF False, don't set the object as object attribute in dispatch
    key_name = 'author'
    
    def dispatch(self, request, *args, **kwargs):
        if self.set_as_attr and self.key_name in kwargs:
            setattr(self, self.key_name, self.get_author(kwargs[self.key_name]))
        return super(AuthorKwargsMixin, self).dispatch(request, *args, **kwargs)
    
    def get_author(self, name):
        return get_object_or_404(User, username=name)
        
    def get_context_data(self, **kwargs):
        context = super(AuthorKwargsMixin, self).get_context_data(**kwargs)
        if hasattr(self, self.key_name):
            context[self.key_name] = getattr(self, self.key_name)
        return context

class DateKwargsMixin(AuthorKwargsMixin):
    """
    Get common date kwargs (year, month, day) to set them as object attributes
    
    This does not check anything, kwargs rules have to be in your view or urls map
    """
    date_kwarg_names = ['year', 'month', 'week', 'day']
    
    def dispatch(self, request, *args, **kwargs):
        for name in self.date_kwarg_names:
            if name in kwargs:
                setattr(self, name, int(kwargs[name]))
        return super(DateKwargsMixin, self).dispatch(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(DateKwargsMixin, self).get_context_data(**kwargs)
        for name in self.date_kwarg_names:
            context[name] = getattr(self, name, None)
        context['target_date'] = datetime.date(getattr(self, 'year', 1977), getattr(self, 'month', 1), getattr(self, 'day', 1))
        return context

class DatebookCalendarMixin(DateKwargsMixin):
    """
    Datebook calendar mixin
    """
    calendar_obj = DatebookCalendar
    
    def get_datebook(self, filters):
        return get_object_or_404(Datebook, author__username=self.kwargs['author'], **filters)
    
    def get_dayentry_list(self, filters={}):
        return self.object.dayentry_set.filter(**filters).order_by('activity_date')
    
    def get_calendar(self, *args, **kwargs):
        return self.calendar_obj(*args, **kwargs)
