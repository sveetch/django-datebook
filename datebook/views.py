# -*- coding: utf-8 -*-
"""
Page document views
"""
import datetime
import calendar

from django.conf import settings
from django import http
from django.shortcuts import get_object_or_404
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from datebook.models import Datebook, DayEntry
from datebook.mixins import AuthorKwargsMixin, DateKwargsMixin, DatebookCalendarMixin
from datebook.forms import DatebookForm, DayEntryForm
from datebook.utils import week_from_date

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

class DatebookAuthorView(generic.TemplateView):
    """
    User datebook index
    
    Display all year that have one or more Datebooks for the given user
    """
    template_name = "datebook/author_index.html"
    
    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(User, username=self.kwargs['author'])
        
        context = {
            'author': self.object,
            'object_list': Datebook.objects.filter(author=self.object).dates('period', 'year'),
        }
        
        return self.render_to_response(context)

class DatebookYearView(DateKwargsMixin, generic.TemplateView):
    """
    Datebook year view
    
    Display the twelve months of the given year with link and infos for the 
    existing datebooks
    """
    template_name = "datebook/datebook_year.html"
        
    def get_context_data(self, **kwargs):
        context = super(DatebookYearView, self).get_context_data(**kwargs)
        
        _curr = datetime.date.today()
        # Get all datebooks for the given year
        queryset = self.object.datebook_set.filter(period__year=self.year).order_by('period')[0:13]
        _datebook_map = dict(map(lambda x: (x.period.month, x), queryset))
        # Fill the finded datebooks in the month map, month without datebook will have 
        # None instead of a Datebook instance
        datebooks_map = [(name, _datebook_map.get(i)) for i, name in enumerate(calendar.month_name) if i>0]
        
        context.update({
            'year_current': _curr.year,
            'is_current_year': (self.year == _curr.year),
            'datebooks_map': datebooks_map,
        })
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.author
        
        context = self.get_context_data(**kwargs)
        
        return self.render_to_response(context)

class DatebookMonthAddView(DatebookCalendarMixin, generic.View):
    """
    Automatically create the datebook if it does not allready exists for the "author+year+month" 
    kwargs given, then redirect to its page.
    
    If the Datebook allready exists for the given kwargs, raise a "Http404"
    """
    def get(self, request, *args, **kwargs):
        if Datebook.objects.filter(author=self.author, period__year=self.year, period__month=self.month).count()>0:
            raise http.Http404
        
        d = self.author.datebook_set.create(period=datetime.date(year=self.year, month=self.month, day=1))
        
        return http.HttpResponseRedirect(d.get_absolute_url())


class DatebookMonthFormView(DatebookCalendarMixin, generic.CreateView):
    """
    Unused, actually "DatebookMonthAddView" does the job
    """
    model = Datebook
    context_object_name = "datebook"
    template_name = "datebook/datebook_month_form.html"
    form_class = DatebookForm


class DatebookMonthView(DatebookCalendarMixin, generic.TemplateView):
    """
    Datebook month details view
    
    Get the Calendar for the given year+month then fill it with day entries
    """
    template_name = "datebook/datebook_month.html"
    
    def get_calendar(self, day_filters={}):
        # Add current day if the datebook period is the current month+year
        current_day = None
        _curr = datetime.date.today()
        if _curr.replace(day=1) == self.object.period:
            current_day = _curr
        
        _cal = super(DatebookMonthView, self).get_calendar()
        
        return {
            "weekheader": _cal.formatweekheader(),
            "month": _cal.formatmonth(self.object.period.year, self.object.period.month, dayentries=self.get_dayentry_list(day_filters), current_day=current_day),
        }
        
    def get_context_data(self, **kwargs):
        context = super(DatebookMonthView, self).get_context_data(**kwargs)
        context.update({
            'datebook': self.object,
            'datebook_calendar': self.get_calendar(),
        })
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        
        context = self.get_context_data(**kwargs)
        
        return self.render_to_response(context)


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
    pass


class DayEntryFormEditView(DayEntryBaseFormView, generic.UpdateView):
    """
    DayEntry form edit view
    """
    def get_object(self):
        """
        Add required args to form instance
        """
        return self.datebook.dayentry_set.get(activity_date__day=self.day)


class DatebookWeekView(DatebookCalendarMixin, generic.TemplateView):
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
