# -*- coding: utf-8 -*-
"""
Forms for month forms
"""
from django.conf import settings
from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper

from datebook.models import Datebook
from datebook.forms import CrispyFormMixin
from datebook.utils.imports import safe_import_module

class DatebookForm(CrispyFormMixin, forms.Form):
    """
    Datebook form
    """
    crispy_form_helper_path = 'datebook.forms.crispies.month_helper'
    
    def __init__(self, *args, **kwargs):
        self.available_users = kwargs.pop('available_users', [])
        super(DatebookForm, self).__init__(*args, **kwargs)
        super(forms.Form, self).__init__(*args, **kwargs)
        
        self.fields['owner'] = forms.ModelChoiceField(label=_('owner'), queryset=self.available_users, empty_label=None)
        self.fields['period'] = forms.DateField(label=_('period'))
    
    def clean_period(self):
        period = self.cleaned_data['period']
        period = period.replace(day=1)
        
        return period
    
    def save(self, *args, **kwargs):
        instance = Datebook(
            author=self.cleaned_data['owner'],
            period=self.cleaned_data['period']
        )
        instance.save()
        
        return instance


class DatebookNotesForm(CrispyFormMixin, forms.ModelForm):
    """
    Datebook form
    """
    crispy_form_helper_path = 'datebook.forms.crispies.notes_helper'
    
    def __init__(self, *args, **kwargs):
        super(DatebookNotesForm, self).__init__(*args, **kwargs)
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
        # Set the form field for Datebook.notes
        field_helper = safe_import_module(settings.DATEBOOK_TEXT_FIELD_HELPER_PATH)
        if field_helper is not None:
            self.fields['notes'] = field_helper(self, **{'label':_('notes'), 'required':True})
    
    def clean_notes(self):
        """
        Text content validation
        """
        notes = self.cleaned_data.get("notes")
        validation_helper = safe_import_module(settings.DATEBOOK_TEXT_VALIDATOR_HELPER_PATH)
        if validation_helper is not None:
            return validation_helper(self, notes)
        else:
            return notes
    
    class Meta:
        model = Datebook
        fields = ['notes']
