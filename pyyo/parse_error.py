"""Parsing error class & utilities."""

class ParseError(Exception):
    """Exception representing a parsing error."""

    def __init__(self, node, message):
        """Initialize the error.

        Arg:
            node : The node on which the error occured.
            message : The error description message.

        """
        super().__init__()
        self._node = node
        self._message = message

def parse_error(node, message_format, *args, **kwargs):
    """Raise a parse error.

    Arg:
        node (yaml.Event) : The node on which the error occured.
        message_format : Description format of the error.
        *args, **kwargs : Arguments to use to format the description.

    """
    message = message_format.format(*args, **kwargs)
    raise ParseError(node, message)
