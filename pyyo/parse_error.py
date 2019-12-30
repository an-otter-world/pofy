"""Parsing error class & utilities."""

class ParseError(Exception):
    """Exception representing a parsing error."""

    def __init__(self, event, message):
        """Initialize the error.

        Arg:
            event : The event on which the error occured.
            message : The error description message.

        """
        super().__init__()
        self._event = event
        self._message = message

def parse_error(event, message_format, *args, **kwargs):
    """Raise a parse error.

    Arg:
        event (yaml.Event) : The event on which the error occured.
        message_format : Description format of the error.
        *args, **kwargs : Arguments to use to format the description.

    """
    message = message_format.format(*args, **kwargs)
    raise ParseError(event, message)
