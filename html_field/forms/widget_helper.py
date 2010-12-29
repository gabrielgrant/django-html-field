

def make_toolbar_config(allow_tags, exclude_tags=('div',), extra_styles=None, show_source=True):
	""" output a CKEditor menu definition, given an html processor """
	if not exclude_tags:
		exclude_tags = []
	
	def allowed(tag):
		return tag in allow_tags and tag not in exclude_tags
	
	# do format_tags
	format_tags = 'p h1 h2 h3 h4 h5 h6 pre address'.split()
	formats = ';'.join(tag for tag in format_tags if allowed(tag))
	
	# do styles (name, tag, styles_dict, attributes_dict)
	# name and element are required
	# styles_dict and attributes_dict are optional dictionaries
	if extra_styles is None:
		extra_styles = []
	style_map = extra_styles + [
		('Big', 'big'),
		('Small', 'small'),
		('Typewriter', 'tt'),

		('Computer Code', 'code'),
		('Keyboard Phrase', 'kbd'),
		('Sample Text', 'samp'),
		('Variable', 'var'),

		('Deleted Text', 'del'),
		('Inserted Text', 'ins'),

		('Cited Work', 'cite'),
		('Inline Quotation', 'q'),
	]
	styles = [style for style in style_map if allowed(style[0])]
	
	styles_set_keys = ['name', 'element', 'styles', 'attributes']
	styles_set = [dict(zip(styles_set_keys, style)) for style in styles]
	
	# do toolbar
	toolbar_maps = [
		[
			(None, ['Cut','Copy','Paste']),
			(None, ['-']),
			(None, ['Undo','Redo','RemoveFormat']),  # Source may go here
		],
		[
			('a', ['Link', 'Unlink', 'Anchor']),
			(None, '-'),
			('img', 'Image'),
			('table', 'Table'),
			('hr', 'HorizontalRule'),
			(None, 'SpecialChar'),
		],
		[
			('strong', 'Bold'),
			('em', 'Italic'),
			('u', 'Underline'),
			('strike', 'Strikethrough'),
			(None, '-'),
			('sub', 'Subscript'),
			('sup', 'Superscript'),
			(None, '-'),
			('ol', 'NumberedList'),
			('ul', 'BulletedList'),
			('blockquote', 'Blockquote')
		],
	]
	if show_source:
		toolbar_maps[0][-1][1].append('Source')
	if formats:
		toolbar_maps[-1].insert(0, (None, 'Format'))
	
	toolbar = []
	for map_ in toolbar_maps:
		strip = [item for tag, item in map_ if tag is None or allowed(tag)]
		# ensure that lone items are wrapped in a list:
		strip = [item if not isinstance(item, basestring) else [item] for item in strip]
		toolbar.append(sum(strip, []))  # flatten
	
	config = {
		'toolbar': toolbar,
		'stylesSet': styles_set,
		'format_tags': formats
	}
	
	return config

