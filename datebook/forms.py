# -*- coding: utf-8 -*-
"""
Forms
"""
from django import forms
from django.utils.translation import ugettext

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Fieldset, SplitDateTimeField, RowFluid, Column, ButtonHolder, Submit

from datebook.models import Datebook, DayEntry

DATETIME_FORMATS = {
    'input_date_formats': ['%d/%m/%Y'],
    'input_time_formats': ['%H:%M'], 
    'widget': forms.SplitDateTimeWidget(date_format='%d/%m/%Y', time_format='%H:%M'),
}

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
    start_datetime = forms.SplitDateTimeField(label=ugettext('start'), **DATETIME_FORMATS)
    stop_datetime = forms.SplitDateTimeField(label=ugettext('stop'), **DATETIME_FORMATS)

    def __init__(self, datebook, day, *args, **kwargs):
        self.datebook = datebook
        self.daydate = datebook.period.replace(day=day)
        
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
                
        
        self.helper = FormHelper()
        self.helper.form_action = '.'
        self.helper.form_class = 'custom'
        self.helper.form_id = 'datebook-dayentry-form'
        self.helper.layout = Layout(
            RowFluid(
                Column('vacation', css_class='twelve'),
            ),
            RowFluid(
                Column('start_datetime', css_class='five mobile-two'),
                Column('pause', css_class='two mobile-one'),
                Column('stop_datetime', css_class='five mobile-two'),
            ),
            RowFluid(
                Column('content', css_class='twelve'),
            ),
            ButtonHolder(
                Submit('submit', ugettext('Save'), css_class='expand'),
            ),
        )
        
        super(DayEntryForm, self).__init__(*args, **kwargs)
    
    def clean_start_datetime(self):
        start = self.cleaned_data['start_datetime']
        # Day entry can't start before the targeted day date
        if start and start.date() < self.daydate:
            raise forms.ValidationError("You can't start a day before itself")
        # Day entry can't start after the targeted day date
        if start and start.date() > self.daydate:
            raise forms.ValidationError("You can't start a day after itself")
        
        return start
    
    def clean_stop_datetime(self):
        start = self.cleaned_data.get('start_datetime')
        stop = self.cleaned_data['stop_datetime']
        # Day entry can't stop before the start
        if start and stop and stop <= start:
            raise forms.ValidationError("Stop time can't be less or equal to start time")
        # Day entry can't stop more than one day to the targeted day date
        if stop and stop.date() > self.daydate.replace(day=self.daydate.day+1):
            raise forms.ValidationError("Stop time can't be more than the next day")
        
        return stop
    
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
        }