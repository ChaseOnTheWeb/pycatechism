import catechism
from catechism.actions.base import Action
from catechism.utils import simple_request

PARAGRAPHS_SEARCH_SORTBY = ('paragraph', 'relevance',)

def search_decorator(f):
    """Parse parameters common to all search functions: sortby, offset, format."""
    def wrapper(*args, **kwargs):
        data = {}
        
        data['sortby'] = kwargs['sortby'] if 'sortby' in kwargs else PARAGRAPHS_SEARCH_SORTBY[0]
        if data['sortby'] not in PARAGRAPHS_SEARCH_SORTBY:
            raise ValueError, "Unsupported sort method '%s'." % kwargs['sortby']
        
        if 'offset' in kwargs:
            data['offset'] = kwargs['offset']

        data['format'] = kwargs['format'] if 'format' in kwargs else catechism.DEFAULT_FORMAT
        
        data.update(f(*args, **kwargs))
        return data
    return wrapper

class Paragraphs(Action):
    """
    Implements paragraphs/get and paragraphs/search (no advanced search yet).
    """

    @simple_request('get')
    def get(self, query, format=None):
        format = format if format is not None else catechism.DEFAULT_FORMAT

        return {'id': query, 'format': format}

    @simple_request('search')
    @search_decorator
    def search_verse(self, query):
        return {'how': 'verse', 'query': query,}

    @simple_request('search')
    @search_decorator
    def search_text(self, query, include_headings=False, include_footnotes=False):
        return {'how': 'text', 'query': query, 'include_heads': include_headings, 'include_fns': include_footnotes,}

    @simple_request('search')
    @search_decorator
    def search_mixed(self, query):
        return {'how': 'mixed', 'query': query,}

    @simple_request('search')
    @search_decorator
    def search_advanced(self, para_id=None, section=None, verse=None, text=None, include_headings=False, include_footnotes=False):
        data = {'how': 'advanced', 'include_heads': include_headings, 'include_fns': include_footnotes,}

        if para_id is not None:
            data['id'] = para_id
        if section is not None:
            data['section'] = section
        if verse is not None:
            data['verse'] = verse
        if text is not None:
            data['text'] = text

        return data

