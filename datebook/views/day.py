# -*- coding: utf-8 -*-
"""
Day entry views
"""
import datetime

from django.conf import settings
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from braces.views import LoginRequiredMixin

from datebook.models import Datebook, DayEntry
from datebook.mixins import AuthorKwargsMixin, DatebookCalendarMixin, DatebookCalendarAutoCreateMixin, OwnerOrPermissionRequiredMixin
from datebook.forms.day import DayEntryForm
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

    def get_form(self, form_class):
        """
        Add required args to form instance
        """
        return form_class(self.datebook, self.day, **self.get_form_kwargs())
    
    def switch_template(self, request):
        if request.is_ajax():
            return self.ajax_template_name
        return self.template_name
    
    def get(self, request, *args, **kwargs):
        self.template_name = self.switch_template(request)
        self.datebook = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        
        return super(DayEntryBaseFormView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.template_name = self.switch_template(request)
        self.datebook = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        
        return super(DayEntryBaseFormView, self).post(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        """
        Add post form url
        """
        kwargs = super(DayEntryBaseFormView, self).get_form_kwargs()
        kwargs.update({'form_action': '.'})
        return kwargs

    def get_success_url(self):
        return reverse('datebook-author-month', kwargs={
            'author': self.author,
            'year': self.object.activity_date.year,
            'month': self.object.activity_date.month,
        })
        
    def get_next(self):
        return None


class DayEntryFormCreateView(DayEntryBaseFormView, generic.CreateView):
    """
    DayEntry form create view
    """
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
            'form_action': reverse('datebook-author-day-add', kwargs={
                'author': self.author,
                'year': self.year,
                'month': self.month,
                'day': self.day,
            })
        })
        return kwargs


class DayEntryFormEditView(DayEntryBaseFormView, generic.UpdateView):
    """
    DayEntry form edit view
    """
    permission_required = 'datebook.change_dayentry'
    
    def get_object(self):
        """
        Add required args to form instance
        """
        return self.datebook.dayentry_set.get(activity_date__day=self.day)
    
    def get_form_kwargs(self):
        """
        Add post form url
        """
        kwargs = super(DayEntryBaseFormView, self).get_form_kwargs()
        kwargs.update({
            'form_action': reverse('datebook-author-day-edit', kwargs={
                'author': self.author,
                'year': self.year,
                'month': self.month,
                'day': self.day,
            })
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
            return reverse('datebook-author-day-add', kwargs={
                'author': self.author,
                'year': self.year,
                'month': self.month,
                'day': self.day,
            })
        else:
            return reverse('datebook-author-day-edit', kwargs={
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
        
    def get_previous(self):
        try:
            obj = self.object.get_previous_by_activity_date(**{
                'datebook__author': self.author,
                'activity_date__month': self.object.activity_date.month,
                'activity_date__year': self.object.activity_date.year,
            })
            print "FOO", obj
        except DayEntry.DoesNotExist:
            pass
        else:
            return obj
        return None
        
    def get_next(self):
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
        return get_object_or_404(DayEntry, datebook=self.datebook, activity_date=datetime.date(self.year, self.month, self.day))
        #try:
            #obj = DayEntry.objects.get(datebook=self.datebook, activity_date=datetime.date(self.year, self.month, self.day))
        #except DayEntry.DoesNotExist:
            #pass
        #else:
            #return obj
        #return None
    
    def get_context_data(self, **kwargs):
        context = super(DayEntryDetailView, self).get_context_data(**kwargs)
        context.update({
            'datebook': self.datebook,
            'object': self.object,
            'previous_day': self.previous_day,
            'next_day': self.next_day,
        })
        return context
    
    def get(self, request, *args, **kwargs):
        self.datebook = self.get_datebook({'period__year': self.year, 'period__month': self.month})
        self.object = self.get_object()
        self.previous_day = self.get_previous()
        self.next_day = self.get_next()
        
        context = self.get_context_data(**kwargs)
        
        return self.render_to_response(context)

