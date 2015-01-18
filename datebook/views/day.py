# -*- coding: utf-8 -*-
"""
Day entry views
"""
import datetime
from calendar import TextCalendar

from django.conf import settings
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic.edit import DeleteView
from braces.views import LoginRequiredMixin

from datebook.models import Datebook, DayEntry
from datebook.mixins import AuthorKwargsMixin, DatebookCalendarMixin, OwnerOrPermissionRequiredMixin
from datebook.forms.day import DayEntryForm, DayEntryCreateForm
from datebook.utils import week_from_date

class DayEntryBaseFormView(DatebookCalendarMixin, OwnerOrPermissionRequiredMixin):
    """
    DayEntry base form view
    """
    model = DayEntry
    context_object_name = "dayentry"
    template_name = "datebook/day/form.html"
    ajax_template_name = "datebook/day/form_fragment.html"
    form_class = DayEntryForm
    permission_required = 'datebook.add_dayentry'
    raise_exception = True
    
    def switch_template(self, request):
        """
        Switch to the specific Ajax template if request is detected as an Ajax request
        """
        if request.is_ajax():
            return self.ajax_template_name
        return self.template_name
    
    def get_next_day(self):
        """
        Find if there is possible next day
        
        If the possible next day is not out of range of the month's days, returns its 
        day entry if exists, else will returns a simple 'datetime.date object'. The 
        return will allways be a tuple containing the object and the resolved form's 
        url.
        
        Finally if there is no possible next day, returns None.
        """
        calendar = TextCalendar()
        # Get available days from reduced calendar's datas
        month_days = [item for sublist in calendar.monthdayscalendar(self.year, self.month) for item in sublist if item]
        month_range = (month_days[0], month_days[-1])
        
        # Next day is out of range for current month
        if self.day+1 > month_days[-1]:
            return None
        
        # Next day is in range, try to find if its day entry allready exists
        next_day = datetime.date(self.year, self.month, self.day+1)
        try:
            obj = self.datebook.dayentry_set.get(activity_date=next_day)
        except DayEntry.DoesNotExist:
            return next_day, reverse('datebook:day-add', kwargs={
                'author': self.author,
                'year': next_day.year,
                'month': next_day.month,
                'day': next_day.day,
            })
        else:
            return obj, reverse('datebook:day-edit', kwargs={
                'author': self.author,
                'year': next_day.year,
                'month': next_day.month,
                'day': next_day.day,
            })
        
        return None
    
    def get_context_data(self, **kwargs):
        context = super(DayEntryBaseFormView, self).get_context_data(**kwargs)
        context.update({
            'next_day': self.next_day,
            'DATEBOOK_TEXT_FIELD_JS_TEMPLATE': settings.DATEBOOK_TEXT_FIELD_JS_TEMPLATE,
            'DATEBOOK_TEXT_MARKUP_RENDER_TEMPLATE': settings.DATEBOOK_TEXT_MARKUP_RENDER_TEMPLATE,
        })
        return context

    def get_form(self, form_class):
        """
        Add required args to form instance
        """
        return form_class(self.datebook, self.day, **self.get_form_kwargs())
    
    def get_form_kwargs(self):
        """
        Add post form url
        """
        kwargs = super(DayEntryBaseFormView, self).get_form_kwargs()
        kwargs.update({
            'form_action': '.',
            'next_day': self.next_day,
        })
        return kwargs

    def get_success_url(self):
        """
        If 'submit_and_next' button has been used, redirect to the next day form, 
        else redirect to the month view
        """
        if 'submit_and_next' in self.request.POST:
            if self.next_day:
                return self.next_day[1]
        
        return reverse('datebook:month-detail', kwargs={
            'author': self.author,
            'year': self.object.activity_date.year,
            'month': self.object.activity_date.month,
        })
        
    def get(self, request, *args, **kwargs):
        self.template_name = self.switch_template(request)
        self.datebook = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        self.next_day = self.get_next_day()
        return super(DayEntryBaseFormView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.template_name = self.switch_template(request)
        self.datebook = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        self.next_day = self.get_next_day()
        return super(DayEntryBaseFormView, self).post(request, *args, **kwargs)


class DayEntryFormCreateView(DayEntryBaseFormView, generic.CreateView):
    """
    DayEntry form create view
    """
    form_class = DayEntryCreateForm
    
    def get_form_kwargs(self):
        """
        Put the initial data for the datetime start and stop
        
        NOTE: Time start and stop should comes from the User profile settings (date 
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
            },
            'form_action': reverse('datebook:day-add', kwargs={
                'author': self.author,
                'year': self.year,
                'month': self.month,
                'day': self.day,
            }),
        })
        return kwargs


class DayEntryFormEditView(DayEntryBaseFormView, generic.UpdateView):
    """
    DayEntry form edit view
    """
    permission_required = 'datebook.change_dayentry'
    
    def get_object(self):
        return self.datebook.dayentry_set.get(activity_date__day=self.day)
    
    def get_form_kwargs(self):
        """
        Add post form url
        """
        kwargs = super(DayEntryBaseFormView, self).get_form_kwargs()
        kwargs.update({
            'form_action': reverse('datebook:day-edit', kwargs={
                'author': self.author,
                'year': self.year,
                'month': self.month,
                'day': self.day,
            }),
            'next_day': self.next_day,
            'day_to_model_url': reverse('datebook:dayentry-to-daymodel', kwargs={
                'author': self.author,
                'year': self.year,
                'month': self.month,
                'day': self.day,
            }),
            'remove_url': reverse('datebook:day-remove', kwargs={
                'author': self.author,
                'year': self.year,
                'month': self.month,
                'day': self.day,
            }),
        })
        return kwargs


class DayEntryCurrentView(AuthorKwargsMixin, OwnerOrPermissionRequiredMixin, generic.RedirectView):
    """
    Redirect to the form for the current day. If entry allready exists this will 
    redirect to edit form, else to add form.
    
    If the month datebook does not exist for the current day, this will create it 
    before redirect.
    """
    permission_required = 'datebook.add_dayentry'
    raise_exception = True
    permanent = False
    
    def get_current_date(self):
        """
        Get the current date
        """
        today = datetime.date.today()
        self.year = self.kwargs['year'] = today.year
        self.month = self.kwargs['month'] = today.month
        self.day = self.kwargs['day'] = today.day
        return today
    
    def get_datebook(self):
        """
        Get or Create datebook
        """
        try:
            obj = Datebook.objects.get(author__username=self.kwargs['author'], period__year=self.year, period__month=self.month)
        except Datebook.DoesNotExist:
            self.author = get_object_or_404(User, username=self.kwargs['author'])
            obj = Datebook(author=self.author, period=datetime.date(self.year, self.month, 1))
            obj.save()
        else:
            self.author = obj.author
        return obj
    
    def get_redirect_url(self, author):
        """
        Get Create or Edit dayentry url
        """
        today = self.get_current_date()
        datebook = self.get_datebook()
        
        try:
            obj = DayEntry.objects.get(datebook=datebook, activity_date=datetime.date(self.year, self.month, self.day))
        except DayEntry.DoesNotExist:
            return reverse('datebook:day-add', kwargs={
                'author': self.author,
                'year': self.year,
                'month': self.month,
                'day': self.day,
            })
        else:
            return reverse('datebook:day-edit', kwargs={
                'author': self.author,
                'year': self.year,
                'month': self.month,
                'day': self.day,
            })


class DayEntryDetailView(LoginRequiredMixin, DatebookCalendarMixin, generic.TemplateView):
    """
    DayEntry detail view
    """
    model = DayEntry
    template_name = "datebook/day/detail_fragment.html"
        
    def get_previous_day(self):
        try:
            obj = self.object.get_previous_by_activity_date(**{
                'datebook__author': self.author,
                'activity_date__month': self.object.activity_date.month,
                'activity_date__year': self.object.activity_date.year,
            })
        except DayEntry.DoesNotExist:
            pass
        else:
            return obj
        return None
        
    def get_next_day(self):
        try:
            obj = self.object.get_next_by_activity_date(**{
                'datebook__author': self.author,
                'activity_date__month': self.object.activity_date.month,
                'activity_date__year': self.object.activity_date.year,
            })
        except DayEntry.DoesNotExist:
            pass
        else:
            return obj
        return None
        
    def get_object(self, **kwargs):
        today = datetime.date.today()
        obj = get_object_or_404(DayEntry, datebook=self.datebook, activity_date=datetime.date(self.year, self.month, self.day))
        obj.projected = False
        if today <= obj.activity_date:
            obj.projected = True
        return obj
    
    def get_context_data(self, **kwargs):
        context = super(DayEntryDetailView, self).get_context_data(**kwargs)
        context.update({
            'datebook': self.datebook,
            'object': self.object,
            'previous_day': self.previous_day,
            'next_day': self.next_day,
            'DATEBOOK_TEXT_MARKUP_RENDER_TEMPLATE': settings.DATEBOOK_TEXT_MARKUP_RENDER_TEMPLATE,
        })
        return context
    
    def get(self, request, *args, **kwargs):
        self.datebook = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        self.object = self.get_object()
        self.previous_day = self.get_previous_day()
        self.next_day = self.get_next_day()
        
        context = self.get_context_data(**kwargs)
        
        return self.render_to_response(context)
    
class DayEntryDeleteFormView(DayEntryBaseFormView, generic.DeleteView):
    template_name = "datebook/day/delete.html"
    permission_required = 'datebook.delete_dayentry'
    
    def get_context_data(self, **kwargs):
        context = super(DayEntryBaseFormView, self).get_context_data(**kwargs)
        context.update({
            'datebook': self.datebook,
            'DATEBOOK_TEXT_FIELD_JS_TEMPLATE': settings.DATEBOOK_TEXT_FIELD_JS_TEMPLATE,
            'DATEBOOK_TEXT_MARKUP_RENDER_TEMPLATE': settings.DATEBOOK_TEXT_MARKUP_RENDER_TEMPLATE,
        })
        return context
    
    def get_object(self):
        return self.datebook.dayentry_set.get(activity_date__day=self.day)

    def get_form(self, form_class):
        return super(DayEntryBaseFormView, self).get_form(form_class)
    
    def get_form_kwargs(self):
        return super(DayEntryBaseFormView, self).get_form_kwargs()

    def get_success_url(self):
        """
        If 'submit_and_next' button has been used, redirect to the next day form, 
        else redirect to the month view
        """
        return reverse('datebook:month-detail', kwargs={
            'author': self.author,
            'year': self.object.activity_date.year,
            'month': self.object.activity_date.month,
        })
        
