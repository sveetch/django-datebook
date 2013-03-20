# -*- coding: utf-8 -*-
"""
Root url's map for application
"""
from django.conf.urls.defaults import *

from datebook.views import IndexView, DatebookMonthView, DatebookWeekView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='datebook-index'),
    
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', DatebookMonthView.as_view(), name='datebook-month'),
    
    url(r'^(?P<author>\w+)/(?P<year>\d{4})/(?P<month>\d{1,2})/week/(?P<week>\d{1})/$', DatebookWeekView.as_view(), name='datebook-month-week'),
)
