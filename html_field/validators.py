class HTMLValidator(object):
    message = _(u'Enter a valid HTML string.')
    code = 'invalid'

    def __init__(self, stripper, message=None, code=None):
    	self.stripper = stripper
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

        if isinstance(self.regex, basestring):
            self.regex = re.compile(regex)

    def __call__(self, value):
        """
        Validates that the input only contains specified tags.
        """
        try:
        	stripper.strip(value)
        except DisallowedTagError, msg:
        	raise ValidationError('%s %s'%(msg, self.message), code=self.code)
