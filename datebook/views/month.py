# -*- coding: utf-8 -*-
"""
Datebook month views
"""
import datetime

from django.conf import settings
from django import http
from django.views import generic
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from datebook.forms.month import DatebookForm, DatebookNotesForm
from datebook.forms.daymodel import AssignDayModelForm
from datebook.models import Datebook
from datebook.mixins import DatebookCalendarMixin, DatebookCalendarAutoCreateMixin, OwnerOrPermissionRequiredMixin
from datebook.utils import format_seconds_to_clock, get_day_weekno

class DatebookMonthFormView(PermissionRequiredMixin, generic.FormView):
    """
    Datebook create form view
    """
    model = Datebook
    form_class = DatebookForm
    template_name = 'datebook/month/form.html'
    permission_required = 'datebook.add_datebook'
    raise_exception = True

    def get_form(self, form_class):
        excluded_users = Datebook.objects.all().values('author_id').distinct()
        self.available_users = User.objects.all().exclude(pk__in=[v['author_id'] for v in excluded_users]).order_by('username')
        
        if self.available_users.count() == 0:
            return None
        return super(DatebookMonthFormView, self).get_form(form_class)
        
    def get_form_kwargs(self, **kwargs):
        kwargs = super(DatebookMonthFormView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'available_users': self.available_users,
        })
        return kwargs
    
    def form_valid(self, form):
        self.object = form.save()
        return super(DatebookMonthFormView, self).form_valid(form)
    
    def get_success_url(self):
        return self.object.get_absolute_url()


class DatebookMonthGetOrCreateView(DatebookCalendarMixin, OwnerOrPermissionRequiredMixin, generic.View):
    """
    Automatically create the datebook if it does not allready exists for the "author+year+month" 
    kwargs given, then redirect to its page.
    
    If the Datebook allready exists for the given kwargs, raise a "Http404"
    """
    permission_required = 'datebook.add_datebook'
    raise_exception = True
    
    def get(self, request, *args, **kwargs):
        if Datebook.objects.filter(author=self.author, period__year=self.year, period__month=self.month).count()>0:
            raise http.Http404
        
        d = self.author.datebook_set.create(period=datetime.date(year=self.year, month=self.month, day=1))
        
        return http.HttpResponseRedirect(d.get_absolute_url())


class DatebookMonthCurrentView(DatebookCalendarAutoCreateMixin, OwnerOrPermissionRequiredMixin, generic.View):
    """
    Automatically create the datebook if it does not allready exists for the "author" 
    kwarg and the current month, then redirect to its page.
    
    If the Datebook allready exists for the given kwargs, directly redirect to it
    """
    def get(self, request, *args, **kwargs):
        self.get_current_date()
        
        q = Datebook.objects.filter(author=self.author, period__year=self.year, period__month=self.month)
        
        if q.count()>0:
            d = q.order_by('period')[0:1][0]
        else:
            d = self.author.datebook_set.create(period=datetime.date(year=self.year, month=self.month, day=1))
        
        return http.HttpResponseRedirect(d.get_absolute_url())

class DatebookMonthView(LoginRequiredMixin, DatebookCalendarMixin, FormMixin, generic.TemplateView):
    """
    Datebook month details view
    
    Get the Calendar for the given year+month then fill it with day entries
    
    Accept POST request for the AssignDayModelForm form that fill days from a day model.
    """
    template_name = "datebook/month/calendar.html"
    form_class = AssignDayModelForm

    def get_calendar(self, day_filters={}):
        """
        Where we get the Datebook's calendar and crawl it to compute some 
        values about its weeks and days
        """
        current_day = datetime.date.today()
        
        # Init the calendar object
        _cal = super(DatebookMonthView, self).get_calendar()
        
        # Get month weeks structure, removing days that are not month's days (equal to 0)
        week_days = [filter(None, item) for item in _cal.monthdayscalendar(self.object.period.year, self.object.period.month)]
        weeks_totals = [{'current': False, 'active': False, 'elapsed_seconds':0, 'overtime_seconds':0, 'vacations':0} for i in range(0, len(week_days))]
        # Tag the current week if we are on a current month
        if current_day.year == self.object.period.year and current_day.month == self.object.period.month:
            for i, item in enumerate(weeks_totals, start=0):
                if current_day.day in week_days[i]:
                    item['current'] = True
                    break
        
        # Calculate total elapsed time for worked days and total vacations
        day_entries = self.get_dayentry_list(day_filters)
        total_elapsed_seconds = total_overtime_seconds = total_vacation = 0
        
        for item in day_entries:
            # Find the day's week number
            weekno = get_day_weekno(week_days, item.activity_date.day)
            week = weeks_totals[weekno]
            
            # Default value for day's mark used in calendar template for a day equal or after the current day
            item.projected = False
            
            # Do not calculate future days (from current day and further)
            if current_day <= item.activity_date:
                item.projected = True
                continue
            # Mark the day's week as active (the week have days that are not projections)
            else:
                weeks_totals[weekno]['active'] = True
            
            # Do not calculate vacations days
            if item.vacation:
                total_vacation += 1
                weeks_totals[weekno]['vacations'] += 1
                continue
            
            # Compute totals (for months and weeks)
            total_elapsed_seconds += item.get_elapsed_seconds()
            total_overtime_seconds += item.get_overtime_seconds()
            weeks_totals[weekno]['elapsed_seconds'] += item.get_elapsed_seconds()
            weeks_totals[weekno]['overtime_seconds'] += item.get_overtime_seconds()
        
        
        # Post process week totals for some additional values
        for item in weeks_totals:
            item['elapsed_time'] = format_seconds_to_clock(item['elapsed_seconds'])
            item['overtime_time'] = format_seconds_to_clock(item['overtime_seconds'])
            
        
        calendar_datas = {
            "days": [item.day for item in _cal.itermonthdates(self.object.period.year, self.object.period.month) if item.month == self.object.period.month],
            "weekheader": _cal.formatweekheader(),
            "weeks_totals": weeks_totals,
            "month": _cal.formatmonth(self.object.period.year, self.object.period.month, dayentries=day_entries, current_day=current_day),
            "elapsed_seconds": 0,
            "elapsed_time": None,
            "overtime_seconds": 0,
            "overtime_time": None,
            "vacations": 0,
        }
        
        # Crawl all weeks to calculate month totals
        for item in weeks_totals:
            calendar_datas['elapsed_seconds'] += item['elapsed_seconds']
            calendar_datas['overtime_seconds'] += item['overtime_seconds']
            calendar_datas['vacations'] += item['vacations']
            
        calendar_datas['elapsed_time'] = format_seconds_to_clock(calendar_datas['elapsed_seconds'])
        calendar_datas['overtime_time'] = format_seconds_to_clock(calendar_datas['overtime_seconds'])
        
        return calendar_datas
    
    def get_day_models(self):
        """
        Get and return author's day models
        """
        return self.author.daymodel_set.all().order_by('title').values('id', 'title')
        
    def get_context_data(self, **kwargs):
        context = super(DatebookMonthView, self).get_context_data(**kwargs)
        context.update({
            'datebook': self.object,
            'daymodels_form': self.form,
            'datebook_calendar': self.calendar,
            'day_models': self.get_day_models(),
            'DATEBOOK_TEXT_MARKUP_RENDER_TEMPLATE': settings.DATEBOOK_TEXT_MARKUP_RENDER_TEMPLATE,
        })
        return context
        
    def get_form_kwargs(self, **kwargs):
        kwargs = super(DatebookMonthView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'author': self.author,
            'datebook': self.object,
            'daychoices': self.calendar['days'],
        })
        return kwargs

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        form.save()
        return super(DatebookMonthView, self).form_valid(form)
 
    def get_success_url(self):
        return self.object.get_absolute_url()
   
    def get(self, request, *args, **kwargs):
        self.object = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        self.calendar = self.get_calendar()
        
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        
        return self.render_to_response(self.get_context_data(**kwargs))
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        self.calendar = self.get_calendar()
        
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        
        if self.form.is_valid():
            return self.form_valid(self.form)
        else:
            return self.form_invalid(self.form)


class DatebookNotesFormView(DatebookCalendarMixin, OwnerOrPermissionRequiredMixin, generic.UpdateView):
    """
    Datebook create form view
    """
    model = Datebook
    form_class = DatebookNotesForm
    template_name = 'datebook/month/notes_form.html'
    permission_required = 'datebook.change_datebook'
    raise_exception = True
    
    def get_object(self):
        self.datebook = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        self.author = self.datebook.author
        return self.datebook
    
    def get_success_url(self):
        return self.object.get_absolute_url()
        
    def get_context_data(self, **kwargs):
        context = super(DatebookNotesFormView, self).get_context_data(**kwargs)
        context.update({
            'DATEBOOK_TEXT_FIELD_JS_TEMPLATE': settings.DATEBOOK_TEXT_FIELD_JS_TEMPLATE,
            'DATEBOOK_TEXT_MARKUP_RENDER_TEMPLATE': settings.DATEBOOK_TEXT_MARKUP_RENDER_TEMPLATE,
        })
        return context
