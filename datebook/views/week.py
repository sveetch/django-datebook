# -*- coding: utf-8 -*-
"""
Datebook week views

DEPRECATED
"""
import calendar

from django import http
from django.views import generic

from braces.views import LoginRequiredMixin

from datebook.mixins import DatebookCalendarMixin

class DatebookWeekView(LoginRequiredMixin, DatebookCalendarMixin, generic.TemplateView):
    """
    Datebook month week details view
    
    Get the week days from the calendar for the given year+month then merge it with 
    associated day entries
    """
    template_name = "datebook/week.html"
    
    def find_weekday_range(self):
        # week number is indexed on 1 in urls, but we use it at a position item in 
        # returned list, so we turn it to indexed on 0
        week = self.week-1
        
        try:
            weekdays = calendar.Calendar().monthdatescalendar(self.year, self.month)[week]
        except IndexError:
            raise http.Http404
        
        # Calendar fill the grid with previous or past month days, so we filter them to 
        # return only the current month days
        _f = lambda x: x.year == self.year and x.month == self.month
        return filter(_f, weekdays)
    
    def get_dayentry_list(self, *args, **kwargs):
        """Improve the queryset to get only the days for the given week"""
        if len(self.weekdays)>1:
            _f = {'activity_date__gte': self.weekdays[0], 'activity_date__lte': self.weekdays[-1]}
        else:
            _f = {'activity_date': self.weekdays[0]}
        return super(DatebookWeekView, self).get_dayentry_list(_f)
    
    def get_context_data(self, **kwargs):
        context = super(DatebookWeekView, self).get_context_data(**kwargs)
        
        # Filter query set on the week days
        self.weekdays = self.find_weekday_range()
        dayentry_list = self.get_dayentry_list()
        # Make an empty dict (index on date) of weekdays
        _w = dict(map(lambda x: (x, None), self.weekdays))
        # Make a dict from the day entry and merge it in the weekdays
        _w.update(dict(map(lambda x: (x.activity_date, x), dayentry_list)))
        
        context.update({
            'datebook': self.object,
            'week': self.week,
            # For django templates loop we need to have a sorted list
            'weekdays': [(key, _w[key]) for key in sorted(_w.iterkeys())],
        })
        return context
    
    def get(self, request, *args, **kwargs):
        # Week number can't be empty or zero (index on 1 for humans)
        if not self.week:
            raise http.Http404
        
        self.object = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        
        context = self.get_context_data(**kwargs)
        
        return self.render_to_response(context)
