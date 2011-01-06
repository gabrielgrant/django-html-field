from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext as _

class HTMLField(forms.CharField):
    default_error_messages = {
        'invalid': _(u'Enter a valid HTML.'),
    }
    #default_validators = [validators.validate_email]
    
    def __init__(self, html_cleaner=None, *args, **kwargs):
    	self.html_cleaner = html_cleaner
    	super(HTMLField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(HTMLField, self).clean(value)
        try:
        	value = self.html_cleaner.clean(value)
        except ValueError, e:
        	raise ValidationError(*e.args)
        return value
