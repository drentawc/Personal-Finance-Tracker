import re

from django.conf import settings
from django.contrib.auth.decorators import login_required


class RequireLoginMiddleware(object):
    """
    Middleware component that wraps the login_required decorator around
    matching URL patterns. To use, add the class to MIDDLEWARE_CLASSES and
    define LOGIN_REQUIRED_URLS and LOGIN_REQUIRED_URLS_EXCEPTIONS in your
    settings.py. For example:
    ------
    LOGIN_REQUIRED_URLS = (
        r'/topsecret/(.*)$',
    )
    LOGIN_REQUIRED_URLS_EXCEPTIONS = (
        r'/topsecret/login(.*)$',
        r'/topsecret/logout(.*)$',
    )
    ------
    LOGIN_REQUIRED_URLS is where you define URL patterns; each pattern must
    be a valid regex.

    LOGIN_REQUIRED_URLS_EXCEPTIONS is, conversely, where you explicitly
    define any exceptions (like login and logout URLs).
    """
    #need for one time initialization, here response is a function which will be called to get response from view/template
    def __init__(self, response):
        self.get_response = response
        self.required = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS)
        self.exceptions = tuple(re.compile(url)for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS)

    def __call__(self, request):
        #any code written here will be called before requesting response
        response = self.get_response(request)
        #any code written here will be called after response
        return response

    #this is called before requesting response
    def process_view(self, request, view_func, view_args, view_kwargs):
        #if authenticated return no exception
        if request.user.is_authenticated:
            return None
        #if found in allowed exceptional urls return no exception
        for url in self.exceptions:
            if url.match(request.path):
                return None
        #return login_required()
        for url in self.required:
            if url.match(request.path):
                return login_required(view_func)(request, *view_args, **view_kwargs)
        #default case, no exception
        return None