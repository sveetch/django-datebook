"""
Crispy forms layouts
"""
from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Row, Column, HTML, Div, Field, ButtonHolder, ButtonHolderPanel, ButtonGroup, Panel, Submit

def day_helper(form_tag=True, form_action='.', **kwargs):
    """
    DayEntry's form layout helper
    
    TODO: for daymodel form compatibility: remove vacation and all buttons and links except the standard "Save"
    """
    helper = FormHelper()
    helper.form_action = form_action
    helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    
    # Tuple containing next day date and resolved url to its form
    next_day = kwargs.pop('next_day', None)
    # Mode to ensure compatibility with DayToDayModelForm (just a save button and no vacation)
    day_to_model_mode = kwargs.pop('day_to_model_mode', False)
    # Resolved url to the 'DayToDayModelForm' form
    day_to_model_url = kwargs.pop('day_to_model_url', None)
    
    # Menu elements (buttons and links)
    menu_elements = []
    
    # For form's buttons
    buttons = [Submit('submit', _('Save'))]
    if not day_to_model_mode and next_day:
        buttons.append(Submit('submit_and_next', _('Save and continue to next day')))
    menu_elements.append(
        Div(
            ButtonGroup(
                *buttons,
                css_class='right'
            ),
            css_class='clearfix'
        )
    )
        
    # For some links under the form's buttons
    links = []
    if not day_to_model_mode:
        if next_day:
            links.append( 
                Div(
                    HTML('<a class="button tiny secondary" href="{0}">'.format(next_day[1])),
                    HTML(_('Pass and continue to next day')),
                    HTML('</a>'),
                )
            )
        if day_to_model_url:
            links.append( 
                Div(
                    HTML('<a class="button tiny secondary" href="{0}">'.format(day_to_model_url)),
                    HTML(_('Use it as a day model')),
                    HTML('</a>'),
                )
            )
    if links:
        menu_elements.append(
            Div(
                ButtonGroup(
                    *links,
                    css_class='right'
                ),
                css_class='clearfix'
            )
        )
    
    # Menu where belong the buttons and links
    menu = Panel(
        *menu_elements,
        css_class='text-right'
    )
    
    # Build the full layout
    helper.layout = Layout(
        Row(
            Column('vacation', css_class='small-6 medium-4 medium-offset-8 text-right'),
        ),
        Row(
            Column('start_datetime', css_class='small-6 medium-4'),
            Column('pause', css_class='small-6 medium-2'),
            Column('stop_datetime', css_class='small-6 medium-4'),
            Column('overtime', css_class='small-6 medium-2'),
            css_class='opacited'
        ),
        Row(
            Column('content', css_class='small-12'),
            css_class='opacited'
        ),
        menu,
    )
    # Replace 'vacation' field with 'title' field for DayToDayModelForm form
    if day_to_model_mode:
        helper.layout.pop(0)
        helper.layout.insert(0,
            Row(
                Column('title'),
            ),
        )

    return helper


def month_helper(form_tag=True):
    """
    Datebook's month form layout helper
    """
    helper = FormHelper()
    helper.form_action = '.'
    helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    
    # Build the full layout
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
    
    # Build the full layout
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

def assign_daymodel_helper(form_tag=True, form_action='.', **kwargs):
    """
    AssignDayModelForm form layout helper
    """
    helper = FormHelper()
    helper.form_action = form_action
    #helper.attrs = {'data_abide': ''}
    helper.form_tag = form_tag
    helper.form_id = "daymodel-menu-chooser-form"
    
    # Build the full layout
    helper.layout = Layout(
        Row(
            Column(
                Field(
                    'days',
                    wrapper_class='hide',
                ),
                Field(
                    'daymodel',
                    wrapper_class='hide-label',
                ),
                css_class='medium-9'
            ),
            Column(
                Submit(
                    'submit',
                    _('Ok'),
                    css_class='postfix',
                ),
                css_class='medium-3'
            ),
            css_class='collapse postfix-round',
        ),
    )
    
    return helper
