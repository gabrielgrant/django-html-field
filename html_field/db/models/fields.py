from django.core.exceptions import ValidationError
from django.db import models
from html_field import forms.HTMLField
from django.contrib import admin
import html_field.widgets

class HTMLField(models.TextField):
    """
    A string field for HTML content.
    It uses the CKEditor widget in forms, if available.
    """
    #default_validators = [validators.validate_email]
    description = _("HTML content")

    def __init__(self, html_cleaner, *args, **kwargs):
        self.html_cleaner = html_cleaner
        super(HTMLField, self).__init__(self, *args, **kwargs)

    def formfield(self, **kwargs):
        # Passing the HTMLProcessor to forms.HTMLField means that
        # the value will be validated twice. This is acceptable since we want
        # the value in the form field (to pass into widget for example).
        defaults = {
            'form_class': forms.HTMLField,
            'html_cleaner': self.html_cleaner
        }
        defaults.update(kwargs)

        if defaults['widget'] == admin.widgets.AdminTextareaWidget:
            defaults['widget'] = html_field.widgets.AdminHTMLWidget
        
        return super(HTMLField, self).formfield(**defaults)
    def clean(self, value):
        """
        Validates the given value using the provided HTMLCleaner
        and returns its "cleaned" value as a Python object.

        Raises ValidationError for any errors.
        """
        value = super(HTMLField, self).clean(value)
        try:
        	value = self.html_cleaner.clean(value)
        except ValueError, e:
        	raise ValidationError(*e.args)
        return value


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^html_field\.db\.models\.fields\.HTMLField"])
except ImportError:
    pass

