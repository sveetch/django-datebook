# -*- coding: utf-8 -*-
"""
Root url's map for application
"""
from django.conf.urls.defaults import *

from datebook.views import (IndexView, DatebookAuthorView, DatebookYearView, 
                            DatebookMonthView, DatebookMonthAddView, DatebookWeekView,
                            DayEntryFormCreateView, DayEntryFormEditView)

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='datebook-index'),
    
    url(r'^(?P<author>\w+)/$', DatebookAuthorView.as_view(), name='datebook-author'),
    
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/$', DatebookYearView.as_view(), name='datebook-author-year'),
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/add/(?P<month>\d{1,2})/$', DatebookMonthAddView.as_view(), name='datebook-author-month-add'),
    
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', DatebookMonthView.as_view(), name='datebook-author-month'),
    #url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/form/$', DatebookMonthFormView.as_view(), name='datebook-author-month-form'),
    
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/week/(?P<week>\d{1})/$', DatebookWeekView.as_view(), name='datebook-author-month-week'),
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/add/(?P<day>\d{1,2})/$', DayEntryFormCreateView.as_view(), name='datebook-author-day-add'),
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/edit/$', DayEntryFormEditView.as_view(), name='datebook-author-day-edit'),
)
