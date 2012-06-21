import json, urllib2
from functools import wraps

class RequestWithMethod(urllib2.Request):
    """
    Subclass of the standard urllib2.Request that can accept a custom method

    Source: http://stackoverflow.com/a/6312600
    """
    def __init__(self, *args, **kwargs):
        self._method = kwargs.pop('method', None)
        urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self):
        return self._method if self._method else super(RequestWithMethod, self).get_method()

def simple_request(path, method=None):
    """
    Decorator for simple API calls (path + data + method) on methods of Action
    subclasses

    Decorator parameters:
    :param str path: URL fragment for this specific API call (appended to
                     action URL base)
    :param str method (optional): HTTP method to use (defaults to GET)

    Methods decorated should return a dict of data parameters.
    """

    method = method if method is not None else 'GET'
    def outer_wrapper(f):
        def wrapper(self, *args, **kwargs):
            data = f(self, *args, **kwargs)

            response = self.core.make_request(self.action_base + path, data=data, method=method)
            headers = response.info()

            if headers.getsubtype() != 'json':
                raise ValueError, "Expected Content-Type of application/json, received %s" % headers.gettype()

            data = json.loads(response.read(), encoding=headers.getparam('charset'))

            # Bug? In paragraphs/search, set 'how' to verse, 'query' to consubstantial. errors is set, but okay is 1.
            if 'errors' in data:
                # The API can return several errors at once, but we can only
                # sensibly raise one of them.
                error = data['errors'][0]
                raise ValueError, "Service error %d: %s" % (error['errno'], error['error'])

            return data['results']

        return wraps(f)(wrapper)
    return outer_wrapper

