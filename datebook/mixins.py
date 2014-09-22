# -*- coding: utf-8 -*-
"""
View mixins
"""
import datetime

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.contrib.auth.views import redirect_to_login

from braces.views import PermissionRequiredMixin

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
        context['today'] = datetime.datetime.today()
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


class DatebookCalendarAutoCreateMixin(DatebookCalendarMixin):
    """
    Same as DatebookCalendarMixin but use a get_or_create instead of get_object_or_404 
    so the datebook is automatically created
    """
    def get_current_date(self):
        today = datetime.date.today()
        self.year = self.kwargs['year'] = today.year
        self.month = self.kwargs['month'] = today.month
        self.day = self.kwargs['day'] = today.day
        return today
    
    def get_datebook(self, filters):
        try:
            obj = Datebook.objects.get(author__username=self.kwargs['author'], **filters)
        except Datebook.DoesNotExist:
            author = get_object_or_404(User, username=self.kwargs['author'])
            obj = Datebook(author=author, period=datetime.date(self.year, self.month, self.day))
            obj.save()
        return obj


class OwnerOrPermissionRequiredMixin(PermissionRequiredMixin):
    """
    Act like 'PermissionRequiredMixin' but pass permission test if the user is 
    the object owner.
    
    Object owner must be in a class attribute named "author". With 'AuthorKwargsMixin' 
    usage, you simply have to put just after like this :
    
        class MyView(AuthorKwargsMixin, OwnerOrPermissionRequiredMixin, ....):
            pass
    
    Then you don't have to do anything for the 'author' attribute. This works for any 
    other class that inherit from 'AuthorKwargsMixin'.
    """
    def dispatch(self, request, *args, **kwargs):
        if getattr(self, 'author', None) is None:
            raise ImproperlyConfigured(
                "'OwnerOrPermissionRequiredMixin' requires "
                "'author' attribute to be set.")
        
        # If the user is the object owner pass permission tests 
        # using 'PermissionRequiredMixin' ancestor
        if request.user.is_authenticated() and request.user == self.author:
            return super(PermissionRequiredMixin, self).dispatch(
                request, *args, **kwargs)
        
        # If user is not the Object owner, continue to check for permission
        return super(OwnerOrPermissionRequiredMixin, self).dispatch(
            request, *args, **kwargs)
