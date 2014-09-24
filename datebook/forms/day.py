# -*- coding: utf-8 -*-
"""
Forms for day forms
"""
from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Fieldset, SplitDateTimeField, RowFluid, Column, ButtonHolder, Submit

from datebook.models import DayEntry
from datebook.forms import CrispyFormMixin

DATETIME_FORMATS = {
    'input_date_formats': ['%d/%m/%Y'],
    'input_time_formats': ['%H:%M'], 
    'widget': forms.SplitDateTimeWidget(date_format='%d/%m/%Y', time_format='%H:%M'),
}

class DayEntryForm(CrispyFormMixin, forms.ModelForm):
    """
    DayEntry form
    """
    crispy_form_helper_path = 'datebook.forms.crispies.day_helper'
    
    start_datetime = forms.SplitDateTimeField(label=_('start'), **DATETIME_FORMATS)
    stop_datetime = forms.SplitDateTimeField(label=_('stop'), **DATETIME_FORMATS)

    def __init__(self, datebook, day, *args, **kwargs):
        self.datebook = datebook
        self.daydate = datebook.period.replace(day=day)
        self.next_day = kwargs.pop('next_day', None)
        
        # Args to give to the form layout method
        self.crispy_form_helper_kwargs = {
            'next_day': self.next_day,
            'form_action': kwargs.pop('form_action'),
        }
        
        # Pass initial data for start and stop to their clone with SplitDateTimeField
        if 'start' in kwargs['initial']:
            kwargs['initial']['start_datetime'] = kwargs['initial']['start']
        if 'stop' in kwargs['initial']:
            kwargs['initial']['stop_datetime'] = kwargs['initial']['stop']
        # For existing instance (in edit mode) pass the start and stop values to their 
        # clone with SplitDateTimeField via initial datas
        if kwargs.get('instance'):
            kwargs['initial']['start_datetime'] = kwargs['instance'].start
            kwargs['initial']['stop_datetime'] = kwargs['instance'].stop
                
        
        super(DayEntryForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
    
    def clean_start_datetime(self):
        start = self.cleaned_data['start_datetime']
        # Day entry can't start before the targeted day date
        if start and start.date() < self.daydate:
            raise forms.ValidationError(_("You can't start a day before itself"))
        # Day entry can't start after the targeted day date
        if start and start.date() > self.daydate:
            raise forms.ValidationError(_("You can't start a day after itself"))
        
        return start
    
    def clean_stop_datetime(self):
        start = self.cleaned_data.get('start_datetime')
        stop = self.cleaned_data['stop_datetime']
        # Day entry can't stop before the start
        if start and stop and stop <= start:
            raise forms.ValidationError(_("Stop time can't be less or equal to start time"))
        # Day entry can't stop more than one day to the targeted day date
        if stop and stop.date() > self.daydate.replace(day=self.daydate.day+1):
            raise forms.ValidationError(_("Stop time can't be more than the next day"))
        
        return stop
    
    # TODO: overtime must not be more than effective worked time
    #def clean_overtime(self):
        #overtime = self.cleaned_data.get('overtime')
        #return overtime
    
    # TODO
    #def clean_pause(self):
        #start = self.cleaned_data.get('start_datetime')
        #stop = self.cleaned_data.get('stop_datetime')
        #pause = self.cleaned_data['pause']
        ## Pause time can't be more than elapsed time between start and stop
        #if start and stop and pause and False:
            #raise forms.ValidationError("Pause time is more than the elapsed time")
        
        #return pause
    
    def save(self, *args, **kwargs):
        instance = super(DayEntryForm, self).save(commit=False, *args, **kwargs)
        instance.start = self.cleaned_data['start_datetime']
        instance.stop = self.cleaned_data['stop_datetime']
        instance.datebook = self.datebook
        instance.activity_date = self.daydate
        instance.save()
        
        return instance
    
    class Meta:
        model = DayEntry
        exclude = ('datebook', 'activity_date', 'start', 'stop')
        widgets = {
            'pause': forms.TimeInput(format=DATETIME_FORMATS['input_time_formats'][0]),
            'overtime': forms.TimeInput(format=DATETIME_FORMATS['input_time_formats'][0]),
        }