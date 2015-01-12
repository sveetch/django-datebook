# -*- coding: utf-8 -*-
"""
Application Crumbs
"""
from autobreadcrumbs import site
from django.utils.translation import ugettext_lazy

site.update({
    'datebook:index': ugettext_lazy('Datebooks'),
    'datebook:create': ugettext_lazy('Create a datebook'),
    'datebook:author-detail': '{{ author.username }}',
    'datebook:year-detail': '{{ year }}',
    'datebook:month-detail': '{{ target_date|date:"F Y" }}',
    'datebook:month-notes': ugettext_lazy('Notes for {{ target_date|date:"F Y" }}'),
    'datebook:day-add': ugettext_lazy('Add {{ target_date|date:"l d F Y" }}'),
    'datebook:day-edit': ugettext_lazy('Edit {{ target_date|date:"l d F Y" }}'),
    'datebook:day-remove': ugettext_lazy('Remove {{ target_date|date:"l d F Y" }}'),
    'datebook:day-models': ugettext_lazy('Day models'),
    'datebook:day-model-edit': ugettext_lazy('Edit "{{ daymodel.title }}"'),
    'datebook:dayentry-to-daymodel': ugettext_lazy('Make a model from {{ target_date|date:"l d F Y" }}'),
})
