# -*- coding: utf-8 -*-
"""
Forms
"""
from django import forms
from django.utils.translation import ugettext

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Fieldset, SplitDateTimeField, RowFluid, Column, ButtonHolder, Submit

from datebook.models import Datebook, DayEntry

class DatebookForm(forms.ModelForm):
    """
    Datebook form
    """
    def __init__(self, author=None, *args, **kwargs):
        self.author = author
        
        self.helper = FormHelper()
        self.helper.form_action = '.'
        
        super(DatebookForm, self).__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        instance = super(DatebookForm, self).save(commit=False, *args, **kwargs)
        instance.author = self.author
        instance.save()
        
        return instance
    
    class Meta:
        model = Datebook

class DayEntryForm(forms.ModelForm):
    """
    DayEntry form
    """
    def __init__(self, datebook, day, *args, **kwargs):
        self.datebook = datebook
        self.daydate = datebook.period.replace(day=day)
        
        self.helper = FormHelper()
        self.helper.form_action = '.'
        self.helper.layout = Layout(
            Fieldset(
                ugettext('Working hours'),
                RowFluid(
                    Column('start', css_class='four'),
                    Column('stop', css_class='four'),
                    Column('pause', css_class='two'),
                    Column('vacation', css_class='two'),
                ),
            ),
            Fieldset(
                ugettext('Content'),
                'content',
            ),
            ButtonHolder(
                Submit('submit', ugettext('Save')),
            ),
        )
        
        super(DayEntryForm, self).__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        instance = super(DayEntryForm, self).save(commit=False, *args, **kwargs)
        instance.datebook = self.datebook
        instance.activity_date = self.daydate
        instance.save()
        
        return instance
    
    class Meta:
        model = DayEntry
        exclude = ('datebook', 'activity_date')
