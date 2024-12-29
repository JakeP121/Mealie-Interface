"""Exceptions that can be thrown by Mealie."""

import logging

_LOGGER = logging.getLogger(__name__)


class MealieException(Exception):
    """Base exception for Mealie opetations."""

    def __str__(self) -> str:
        """User friendly string representation of this exception."""
        return "Mealie encountered an unknown exception"

    def log_exception(self):
        """Log an error message."""
        logging.warning(str(self))


class LoginFailed(MealieException):
    """Could not log into this account."""

    def __init__(self, *args: object, username: str) -> None:
        """Init."""
        super().__init__(*args)
        self.username = username

    def __str__(self) -> str:
        """User friendly string representation of this object."""
        return "Failed to log in and get a bearer code for user " + self.username


class InvalidQuery(MealieException):
    """There's a problem with the query parameters."""

    def __init__(self, *args: object, url: str, status_code: int) -> None:
        """Init."""
        super().__init__(*args)
        self.url = url
        self.status_code = status_code

    def __str__(self) -> str:
        """User friendly string representation of this exception."""
        return "Received status code " + self.status_code + " from " + self.url


class CouldNotFind(MealieException):
    """Could not find the thing you're trying to."""

    def __init__(
        self, *args: object, object_name: str, possibilities: set[str] | None = None
    ) -> None:
        """Init."""
        super().__init__(*args)

        self.object_name = object_name
        self.possibilities = possibilities

    def __str__(self) -> str:
        """User friendly string representation of this exception."""
        out = "Could not find " + self.object_name

        if self.possibilities is not None and len(self.possibilities) > 0:
            out = out + ". Did you mean ["
            for p in self.possibilities:
                out = out + p
                if p is not self.possibilities[len(self.possibilities) - 1]:
                    out = out + ", "

            out = out + "]"

        return out


class AlreadyExists(MealieException):
    """Whatever you're trying to do already exists."""

    def __init__(self, *args: object, error_string: str) -> None:
        """Init."""
        super().__init__(*args)
        self.error_string = error_string

    def __str__(self) -> str:
        """User friendly string representation of this object."""
        return self.error_string
