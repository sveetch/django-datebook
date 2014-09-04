# -*- coding: utf-8 -*-
"""
Datebook month views
"""
import datetime

from django import http
from django.views import generic
from django.core.urlresolvers import reverse

from datebook.models import Datebook
from datebook.mixins import DatebookCalendarMixin
from datebook.forms.month import DatebookForm

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


class DatebookMonthFormView(generic.FormView):
    """
    Datebook create form view
    """
    model = Datebook
    form_class = DatebookForm
    template_name = 'datebook/datebook_month_form.html'
    permission_required = 'datebook.add_datebook'
    raise_exception = True
    
    def form_valid(self, form):
        self.object = form.save()
        return super(DatebookMonthFormView, self).form_valid(form)
    
    def get_success_url(self):
        return self.object.get_absolute_url()



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
