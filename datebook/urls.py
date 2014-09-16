# -*- coding: utf-8 -*-
"""
Root url's map for application
"""
from django.conf.urls import *

from datebook.views import IndexView
from datebook.views.author import DatebookAuthorView
from datebook.views.year import DatebookYearView
from datebook.views.month import DatebookMonthView, DatebookMonthAddView, DatebookMonthFormView
from datebook.views.day import DayEntryFormCreateView, DayEntryDetailView, DayEntryFormEditView, DayEntryCurrentView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='datebook-index'),
    
    url(r'^create/$', DatebookMonthFormView.as_view(), name='datebook-create'),
    
    url(r'^(?P<author>\w+)/$', DatebookAuthorView.as_view(), name='datebook-author'),
    
    url(r'^(?P<author>\w+)/current-day/$', DayEntryCurrentView.as_view(), name='datebook-current-day'),
    
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/$', DatebookYearView.as_view(), name='datebook-author-year'),
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/add/(?P<month>\d{1,2})/$', DatebookMonthAddView.as_view(), name='datebook-author-month-add'),
    
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', DatebookMonthView.as_view(), name='datebook-author-month'),
    
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/add/(?P<day>\d{1,2})/$', DayEntryFormCreateView.as_view(), name='datebook-author-day-add'),
    
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', DayEntryDetailView.as_view(), name='datebook-author-day'),
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/edit/$', DayEntryFormEditView.as_view(), name='datebook-author-day-edit'),
)
