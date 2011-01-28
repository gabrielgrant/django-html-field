from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext as _

from html_field.forms.widgets import HTMLWidget, AdminHTMLWidget
from django.contrib import admin

class HTMLField(forms.CharField):
    default_error_messages = {
        'invalid': _(u'Enter valid HTML.'),
    }
    widget = HTMLWidget
    
    def __init__(self, html_cleaner=None, *args, **kwargs):
    	self.html_cleaner = html_cleaner

        if 'widget' in kwargs:
            if kwargs['widget'] == admin.widgets.AdminTextareaWidget:
                kwargs['widget'] = AdminHTMLWidget
    	super(HTMLField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(HTMLField, self).clean(value)
        try:
        	value = self.html_cleaner.clean(value)
        except ValueError, e:
        	raise ValidationError(*e.args)
        return value
