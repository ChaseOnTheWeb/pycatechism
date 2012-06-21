from catechism.actions.base import Action
from catechism.utils import simple_request

class Sections(Action):
    """
    Implements sections/list and sections/get.
    """

    @simple_request('list')
    def list(self, nested=False):
        how = 'nested' if nested else 'flat'

        return {'how': how}

    @simple_request('get')
    def get(self, section):
        return {'id': section}

