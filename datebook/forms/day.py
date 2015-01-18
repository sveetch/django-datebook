# -*- coding: utf-8 -*-
"""
Forms for day forms
"""
from django.conf import settings
from django import forms
from django.utils.translation import ugettext as _

from arrow import Arrow

from datebook.models import DayEntry
from datebook.forms import CrispyFormMixin
from datebook.utils.imports import safe_import_module

DATETIME_FORMATS = {
    'input_date_formats': ['%d/%m/%Y'],
    'input_time_formats': ['%H:%M'], 
    'widget': forms.SplitDateTimeWidget(date_format='%d/%m/%Y', time_format='%H:%M'),
}

class DayBaseFormMixin(object):
    """
    DayBase form mixin
    """
    crispy_form_helper_path = 'datebook.forms.crispies.day_helper'
    crispy_form_helper_kwargs = {}
    
    def fill_initial_data(self, *args, **kwargs):
        # Pass initial data for start and stop to their SplitDateTimeField clones
        if 'start' in kwargs['initial']:
            kwargs['initial']['start_datetime'] = kwargs['initial']['start']
        if 'stop' in kwargs['initial']:
            kwargs['initial']['stop_datetime'] = kwargs['initial']['stop']
            
        # For existing instance (in edit mode) pass the start and stop values to their 
        # clone with SplitDateTimeField via initial datas
        if kwargs.get('instance'):
            kwargs['initial']['start_datetime'] = kwargs['instance'].start
            kwargs['initial']['stop_datetime'] = kwargs['instance'].stop
        
        return kwargs
    
    def init_fields(self, *args, **kwargs):
        self.fields['start_datetime'] = forms.SplitDateTimeField(label=_('start'), **DATETIME_FORMATS)
        self.fields['stop_datetime'] = forms.SplitDateTimeField(label=_('stop'), **DATETIME_FORMATS)
        
        # Set the form field for DayEntry.content
        field_helper = safe_import_module(settings.DATEBOOK_TEXT_FIELD_HELPER_PATH)
        if field_helper is not None:
            self.fields['content'] = field_helper(self, **{'label':_('content'), 'required': False})
    
    def clean_content(self):
        """
        Text content validation
        """
        content = self.cleaned_data.get("content")
        validation_helper = safe_import_module(settings.DATEBOOK_TEXT_VALIDATOR_HELPER_PATH)
        if validation_helper is not None:
            return validation_helper(self, content)
        else:
            return content
    
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
        # Day entry can't stop in more than one futur day from the targeted day date
        if stop and stop.date() > Arrow.fromdate(self.daydate).replace(days=1).date():
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
    

class DayEntryForm(DayBaseFormMixin, CrispyFormMixin, forms.ModelForm):
    """
    DayEntry form
    """
    def __init__(self, datebook, day, *args, **kwargs):
        self.datebook = datebook
        self.daydate = datebook.period.replace(day=day)
        
        # Args to give to the form layout method
        self.crispy_form_helper_kwargs.update({
            'next_day': kwargs.pop('next_day', None),
            'day_to_model_url': kwargs.pop('day_to_model_url', None),
            'form_action': kwargs.pop('form_action'),
            'remove_url': kwargs.pop('remove_url', None),
        })
        
        # Fill initial datas
        kwargs = self.fill_initial_data(*args, **kwargs)
        
        super(DayEntryForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
        # Init some special fields
        kwargs = self.init_fields(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super(DayBaseFormMixin, self).clean()
        content = cleaned_data.get("content")
        vacation = cleaned_data.get("vacation")
        # Content text is only required when vacation is not checked
        if not vacation and not content:
            raise forms.ValidationError(_("Worked days require a content text"))
        
        return cleaned_data
    
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


class DayEntryCreateForm(DayEntryForm):
    def clean(self):
        cleaned_data = super(DayEntryCreateForm, self).clean()
        
        # Validate that there is not allready a day entry for the same day
        try:
            obj = DayEntry.objects.get(datebook=self.datebook, activity_date=self.daydate)
        except DayEntry.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(_("This day entry has allready been created"))
            
        return cleaned_data
