from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext as _

from html_field.forms.widgets import HTMLWidget, AdminHTMLWidget
from html_field.forms.widget_helper import make_toolbar_config
from django.contrib import admin

class HTMLField(forms.Field):
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

    def widget_attrs(self, widget):
        attrs = super(HTMLField, self).widget_attrs(widget) or {}
        try:
            import ckeditor.widgets
        except ImportError:
            ckeditor = None
        if (ckeditor and
            isinstance(widget, ckeditor.widgets.CKEditor) and
            widget.ckeditor_config == 'default'
        ):
            allow_tags = self.html_cleaner.allow_tags
            config = make_toolbar_config(allow_tags=allow_tags)
            attrs['ckeditor_config'] = config
        print attrs
        return attrs
