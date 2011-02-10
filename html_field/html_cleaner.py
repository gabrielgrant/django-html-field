from HTMLParser import HTMLParser
from xml.sax.saxutils import quoteattr
from html_field.exceptions import DisallowedTagError

all_HTML_tags=()
default_allow_attrs=['class', 'style', 'title']
default_allow_attrs_for_tag={
	'a': ['href'],
	'img': ['src', 'alt']
}

def escape_tag(tag):
	# escape the text making up a tag
	# leave "&"s, since those must already be escaped for the doc to be valid
	return tag.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

class HTMLCleaner(HTMLParser):
	def __init__(self,
		indent='  ',
		allow_tags=None,
		allow_attrs=default_allow_attrs,
		allow_attrs_for_tag=default_allow_attrs_for_tag,
		on_disallowed_tag='error',
		indent_content=True
	):
		"""
		indent
		default '  ' (two spaces)
		'' gives no indent, but still splits each tag onto a new line
		None doen't split lines
		
		on_disallowed_tag
		what to do when a disallowed tag is encountered:
		- strip: tags will be removed entirely
		- error: a DisallowedTagError will be raised 
		- escape: text making up the tag will be escaped
		
		indent_content
		if True (defualt) each line of content within tags will be indented
		
		
		"""
		self.indent = indent
		self.allow_tags = allow_tags
		self.allow_attrs = allow_attrs
		self.allow_attrs_for_tag = allow_attrs_for_tag
		if on_disallowed_tag not in ('strip', 'error', 'escape'):
			raise ValueError
		self.on_disallowed_tag = on_disallowed_tag
		self.indent_content = indent_content
		HTMLParser.__init__(self)
	def reset(self):
		self._depth = 0
		self._output = ''
		HTMLParser.reset(self)
		
	@property
	def indent_template(self):
		if self.indent is None:
			return '%s'
		else:
			full_indent = self.indent*self._depth
			if self.indent_content:
				return '\n%s%s\n%s'%(full_indent, '%s', full_indent)
			else:
				return '\n%s%s\n'%(full_indent, '%s')
	
	def handle_start_or_startend(self, tag, attrs):
		if self.allow_tags is not None and tag not in self.allow_tags:
			if self.on_disallowed_tag == 'strip':
				return False, ''
			elif self.on_disallowed_tag == 'error':
				raise DisallowedTagError('Input contains %s tag, which is not allowed.'%tag)
			elif self.on_disallowed_tag == 'escape':
				return False, escape_tag(self.get_starttag_text())
			else:
				raise RuntimeError('on_disallowed_tag must be one of "escape", "error" or "strip"')
		else:
			# this should be cached for speed
			allow_attrs = self.allow_attrs + self.allow_attrs_for_tag.get(tag,[])
			attrs = [(k,v) for k,v in attrs if k in allow_attrs]
			attrs = ' '.join("%s=%s"%(k,quoteattr(v)) for k,v in attrs)
			if attrs:
				content = '%s %s'%(tag, attrs)
			else:
				content = tag
			return True, content
		
	def handle_starttag(self, tag, attrs):
		valid, content = self.handle_start_or_startend(tag, attrs)
		if valid:
			self._output += self.indent_template%'<%s>'%content
			self._depth += 1
		else:
			self._output += content
				
	def handle_startendtag(self, tag, attrs):
		valid, content = self.handle_start_or_startend(tag, attrs)
		if valid:
			self._output += self.indent_template%'<%s />'%content
		else:
			self._output += content
		
	
	def handle_endtag(self, tag):
		if self.allow_tags is not None and tag not in self.allow_tags:
			if self.on_disallowed_tag == 'strip':
				output = ''
			elif self.on_disallowed_tag == 'error':
				raise DisallowedTagError('Input contains %s endtag, which is not allowed'%tag)
			elif self.on_disallowed_tag == 'escape':
				output = escape_tag('</%s>'%tag)
			else:
				raise RuntimeError('on_disallowed_tag must be one of "escape", "error" or "strip"')
		else:
			self._depth -= 1
			output = self.indent_template%'</%s>'%tag
		self._output += output
	
	def handle_data(self, data):
		self._output += data

	def handle_charref(self, name):
		self._output += '&#%s;' % name

	def handle_entityref(self, name):
		self._output += '&%s;' % name

	def handle_comment(self, data):
		self._output += '<!--%s-->' % data

	def clean(self, data):
		self.reset()
		self.feed(data)
		self.close()
		return self._output
	
	def __repr__(self):
		return """HTMLCleaner(
		indent=%s,
		allow_tags=%s,
		allow_attrs=%s,
		allow_attrs_for_tag=%s,
		on_disallowed_tag=%s,
		indent_content=%s
		)""" % tuple(repr(i) for i in (
		self.indent,
		self.allow_tags,
		self.allow_attrs,
		self.allow_attrs_for_tag,
		self.on_disallowed_tag,
		self.indent_content
		))
def test():
	import html_cleaner
	reload(html_cleaner)
	s = html_cleaner.HTMLCleaner(allow_tags=['a'])
	print s.clean('<p>hello! i am a <a href="here.html" onClick="javascript:doThat();">link</a>, and <em>you</em> are a <h1>title</h1></p>')
