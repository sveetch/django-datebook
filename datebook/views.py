# -*- coding: utf-8 -*-
"""
Page document views
"""
import datetime
from calendar import Calendar

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views import generic

from datebook.models import Datebook, DayEntry
from datebook.calendars import DatebookHTMLCalendar

class IndexView(generic.list.ListView):
    """
    Index view
    """
    model = Datebook
    template_name = "datebook/index.html"
    paginate_by = None

class DatebookDetailsMixin(object):
    """
    Datebook details mixin
    """
    def get_object(self, filters):
        return get_object_or_404(Datebook, author__username=self.kwargs['author'], **filters)
    
    def get_dayentry_list(self, filters={}):
        return self.object.dayentry_set.filter(**filters).order_by('activity_date')
    
    def get_calendar(self, day_filters={}):
        # Add current day if the datebook period is the current month+year
        current_day = None
        _curr = datetime.date.today()
        if _curr.replace(day=1) == self.object.period:
            current_day = _curr.day
        
        # Get the day items
        day_items = {}
        for item in self.get_dayentry_list(day_filters):
            day_items[item.activity_date.day] = item
        
        calendar_table = DatebookHTMLCalendar(day_items=day_items, current_day=current_day)
        
        return calendar_table.formatmonth(self.object.period.year, self.object.period.month)


class DatebookMonthView(DatebookDetailsMixin, generic.TemplateView):
    """
    Datebook month details view
    
    Get the Calendar for the given year+month then fill it with day entries
    """
    template_name = "datebook/datebook_month.html"
    
    def get(self, request, *args, **kwargs):
        self.year, self.month = int(self.kwargs['year']), int(self.kwargs['month']) # This should go in the dispatch
        self.object = self.get_object({'period__year': self.year, 'period__month': self.month})
        
        context = {
            'datebook': self.object,
            'datebook_calendar': self.get_calendar(),
        }
        
        return self.render_to_response(context)

class DatebookWeekView(DatebookDetailsMixin, generic.TemplateView):
    """
    Datebook month week details view
    
    Get the week days from the calendar for the given year+month then merge it with 
    associated day entries
    """
    template_name = "datebook/datebook_month_week.html"
    
    def find_weekday_range(self):
        # week number is indexed on 1 in urls, but we use it at a position item in 
        # returned list, so we turn it to indexed on 0
        week = self.week-1
        
        try:
            weekdays = Calendar().monthdatescalendar(self.year, self.month)[week]
        except IndexError:
            raise Http404
        
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
        print _f
        return super(DatebookWeekView, self).get_dayentry_list(_f)
    
    def get(self, request, *args, **kwargs):
        self.year, self.month = int(self.kwargs['year']), int(self.kwargs['month'])
        self.week = int(self.kwargs['week'])
        # Week number can't be empty or zero (index on 1 for humans)
        if not self.week:
            raise Http404
        
        self.object = self.get_object({'period__year': self.year, 'period__month': self.month})
        
        # Filter query set on the week days
        self.weekdays = self.find_weekday_range()
        dayentry_list = self.get_dayentry_list()
        # Make an empty dict (index on date) of weekdays
        _w = dict(map(lambda x: (x, None), self.weekdays))
        # Make a dict from the day entry and merge it in the weekdays
        _w.update(dict(map(lambda x: (x.activity_date, x), dayentry_list)))
        
        context = {
            'datebook': self.object,
            'month_week': self.week,
            # For django templates loop we need to have a sorted list
            'weekdays': [(key, _w[key]) for key in sorted(_w.iterkeys())],
        }
        
        return self.render_to_response(context)

# To implement ?
class DatebookYearView(generic.TemplateView): pass
class DatebookDayView(generic.TemplateView): pass
