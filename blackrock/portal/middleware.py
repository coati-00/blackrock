from django.conf import settings
from django.core.urlresolvers import RegexURLResolver
import sys


def resolver(request):
    """
    Returns a RegexURLResolver for the request's urlconf.

    If the request does not have a urlconf object, then the default of
    settings.ROOT_URLCONF is used.
    """
    urlconf = getattr(request, "urlconf", settings.ROOT_URLCONF)
    return RegexURLResolver(r'^/', urlconf)


class ValueErrorMiddleware(object):
    def process_exception(self, request, exception):
        # Get the exception info now, in case another exception is thrown
        # later.
        if isinstance(exception, ValueError) and \
            len(exception.args) > 0 and \
                exception.args[0].startswith('invalid literal for int()'):
            return self.handleValueError(request, exception)

    def handleValueError(self, request, exception):
        exc_info = sys.exc_info()
        if settings.DEBUG:
            from django.views import debug
            return debug.technical_500_response(request, *exc_info)
        else:
            '''Return an HttpResponse that displays a friendly message.'''
            callback, param_dict = resolver(request).resolve500()
            return callback(request, **param_dict)
