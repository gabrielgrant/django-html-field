from django import forms
from django.contrib import admin

class InPageJSMedia(forms.Media):
	def __init__(self, media=None, in_page_js=None, **kwargs):
		if in_page_js is not None:
			self._in_page_js = in_page_js
		else:
			self._in_page_js = []
	def render_js(self):
		in_page_js = [u'<script type="text/javascript">\n%s\n</script>' % js for js in self._in_page_js]
		return super(InPageJSMedia, self).render_js() + in_page_js

try:
	import ckeditor.widgets
except ImportError:
	ckeditor = None

if ckeditor:
	class HTMLWidget(ckeditor.widgets.CKEditor):
		pass
	class AdminHTMLWidget(admin.widgets.AdminTextareaWidget, HTMLWidget):
		pass
else:
	HTMLWidget = forms.Textarea
	AdminHTMLWidget = admin.widgets.AdminTextareaWidget
