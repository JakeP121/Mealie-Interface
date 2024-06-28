"""Provides a base class with API endpoint functionality."""

from .Exceptions import InvalidStatusCode


class APIHandler:
    """Base class for API endpoint functionality."""

    def __init__(self, url: str) -> None:
        """Init."""
        self.base_url = url

    def construct_endpoint_url(
        self, endpoint: str, url_params: dict | None = None
    ) -> str:
        """Create an endpoint url from the base url + any parameters."""
        url = self.base_url + "/" + endpoint

        if url_params is None or len(url_params) <= 0:
            return url

        # Add parameters
        url += "?"
        param_index = 0
        for param, value in url_params.items():
            url += param + "=" + str(value)

            if param_index < len(url_params) - 1:
                url += "&"

            param_index += 1

        return url

    def check_response(self, response):
        """Check we got a valid response from the endpoint."""
        if response.status_code < 100 or response.status_code >= 400:
            raise InvalidStatusCode
