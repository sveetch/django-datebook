"""
Crispy forms layouts
"""
from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Fieldset, SplitDateTimeField, Row, Div, Column, HTML, Field, InlineField, SwitchField, ButtonHolder, ButtonHolderPanel, Submit

def day_helper(form_tag=True, form_action='.', has_next=False):
    """
    DayEntry's form layout helper
    """
    helper = FormHelper()
    helper.form_action = form_action
    helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    
    buttons = [
        HTML('<ul class="button-group stack-for-small right"><li>'),
        Submit('submit', _('Save')),
        HTML('</li></ul>'),
    ]
    if has_next:
        buttons = [buttons[0]]+[
            HTML('</li><li>'),
            Submit('submit_and_next', _('Save and continue to next day')),
        ]+buttons[1:]
    
    helper.layout = Layout(
        Row(
            Column('vacation', css_class='small-6 medium-4 medium-offset-8 text-right'),
        ),
        Row(
            Column('start_datetime', css_class='small-4 medium-5'),
            Column('pause', css_class='small-4 medium-2'),
            Column('stop_datetime', css_class='small-4 medium-5'),
            css_class='opacited'
        ),
        Row(
            Column('content', css_class='small-12'),
            css_class='opacited'
        ),
        ButtonHolderPanel(
            *buttons,
            css_class=' clearfix text-right'
        ),
    )

    return helper


def month_helper(form_tag=True):
    """
    Datebook's form layout helper
    """
    helper = FormHelper()
    helper.form_action = '.'
    helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    
    helper.layout = Layout(
        Row(
            Column(
                Field('owner'),
                css_class='small-12 medium-7 hide-label'
            ),
            Column(
                Field('period'),
                css_class='small-12 medium-3 hide-label'
            ),
            Column(
                ButtonHolder(
                    Submit(
                        'submit',
                        _('Save'),
                        css_class='tiny expand',
                    ),
                    css_class='text-right',
                ),
                css_class='small-12 medium-2'
            ),
            css_class='collapse',
        ),
    )
    
    return helper

def year_helper(form_tag=True):
    """
    Datebook's year form layout helper
    """
    helper = FormHelper()
    helper.form_action = '.'
    helper.form_class = "hide-label right clearfix"
    helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    
    helper.layout = Layout(
        Field(
            'year',
            wrapper_class='left',
        ),
        Submit(
            'submit',
            _('New year'),
            css_class='tiny',
        ),
    )
    
    return helper
