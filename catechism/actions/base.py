class Action(object):
    """
    Parent class from which all actions should inherit.
    """

    def __init__(self, core):
        self.core = core

    @property
    def action_base(self):
        """
        The URL fragment for the commands that fall under this action,
        relative to the endpoint URL, with trailing slash.
        """
        return self.__class__.__name__.lower() + '/'

