# -*- coding: utf-8 -*-
"""
Some generic views
"""
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin

class ListAppendView(ListView, FormMixin):
    """
    A view to display an object list with a form to append a new object
    
    This view re-use some code from FormMixin and SimpleListView, sadly it seem not 
    possible to simply mix them.
    
    Need "model" and "form_class" attributes for the form parts and the required one 
    by BaseListView. "get_success_url" method should be filled too.
    
    "locked_form" is used to disable form (like if your list object is closed to new 
    object)
    """
    model = None
    form_class = None
    template_name = None
    paginate_by = None
    locked_form = False
    
    def form_valid(self, form):
        self.object = form.save()
        return super(ListAppendView, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(object_list=self.object_list, form=form))

    def get_locked_form(self, form_class):
        return self.locked_form

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        if self.get_locked_form(form_class):
            return None
        return form_class(**self.get_form_kwargs())
        
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(u"Empty list and '%(class_name)s.allow_empty' is False.".format(class_name=self.__class__.__name__))
        
        context = self.get_context_data(object_list=self.object_list, form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(u"Empty list and '%(class_name)s.allow_empty' is False.".format(class_name=self.__class__.__name__))
        
        if form and form.is_valid():
            return self.form_valid(form)
        elif form:
            return self.form_invalid(form)
        else:
            context = self.get_context_data(object_list=self.object_list, form=form)
            return self.render_to_response(context)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)
