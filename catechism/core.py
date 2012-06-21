import urllib2, json
from urllib import urlencode

import catechism

from catechism import actions
from catechism.utils import RequestWithMethod

class CatechismCore(object):
    """Core class for maintaining authentication info."""

    def __init__(self, username, key, api_endpoint=None):
        self.username = username
        self.key = key
        self.api_endpoint = api_endpoint if api_endpoint else catechism.DEFAULT_API_ENDPOINT

    def make_request(self, command, data={}, method=None):
        """
        Issues HTTP request to API endpoint.

        :param str command: command relative to endpoint URL, e.g. sections/list
        :param dict data: data to send along with the command
        :param str method: HTTP method to use in transmission

        If the method is GET and data is provided, the data is appended to the
        query string; otherwise, it is sent in the request body.
        """

        url = self.api_endpoint + command

        data['username'] = self.username
        data['key'] = self.key

        if method == 'GET' and len(data):
            url = url + '?' + urlencode(data)
            data = None
        else:
            data = urlencode(data)

        request = RequestWithMethod(url, data=data, method=method)
        request.add_header('Accept', 'application/json');
        request.add_header('User-Agent', 'pycatechism/1.0');

        return urllib2.urlopen(request)

class Catechism(object):
    """
    Frontend class for interacting with the catechism API

    This class accepts your username and API key on initialization and sets
    up a registry of actions you can call.  Actions are accessed as attributes
    on the Catechism instance, e.g. <Catechism instance>.paragraphs.get(1200).
    """

    def __init__(self, username, key, api_endpoint=None):
        """
        Setup catechism API object

        :param str username: your API username.
        :param str key: your API key (get one at 
                        http://www.catholiccrossreference.com/request-key.php)
        :param str api_endpoint (optional): the base URL for the catechism API
                                            (include trailing slash)
        """

        self._core = CatechismCore(username, key, api_endpoint)
        self._actions = {}

        for action in actions.DEFAULT_ACTIONS:
            self.add_action(action)

    def __getattr__(self, name):
        if name in self._actions:
            return self._actions[name]

        raise AttributeError, name

    def add_action(self, klass, name=None):
        """
        Add the specified action to the action registry.

        :param class klass: a subclass of catechism.actions.Action
        :param str name (optional): an alternate name for this action
        """

        if name is None:
            name = klass.__name__.lower()

        if name in self._actions:
            raise NameError, 'Name exists.'

        self._actions[name] = klass(self._core)

    def get_actions(self):
        """Return a list of all registered actions."""
        return [x for x in self._actions.keys()]

    def del_action(self, name):
        """
        Delete the specified action from the action registry.

        :param str name: the name (key) of the action in the registry (not the class name!)
        """
        if name in self._actions:
            del self._actions[name]
        else:
            raise NameError, 'Name does not exist.'

