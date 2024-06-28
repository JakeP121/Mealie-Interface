"""Exceptions that can be thrown by REST."""


class InvalidStatusCode(Exception):
    """When the endpoint returns an invalid status code."""

    def __init__(self, *args: object) -> None:
        """Init."""
        super().__init__(*args)
