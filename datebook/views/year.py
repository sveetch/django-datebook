# -*- coding: utf-8 -*-
"""
Datebook year views
"""
import datetime
import calendar

from django.views import generic

from datebook.mixins import DateKwargsMixin

class DatebookYearView(DateKwargsMixin, generic.TemplateView):
    """
    Datebook year view
    
    Display the twelve months of the given year with link and infos for the 
    existing datebooks
    """
    template_name = "datebook/year.html"
        
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

