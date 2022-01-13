import os
import typing as t

import requests

from push_to_3yourmind import exceptions
from push_to_3yourmind import types
from push_to_3yourmind.logger import logger


__all__ = ["BaseAPI"]


class BaseAPI:
    """
    Base class for all namespaced API methods.
    """

    def __init__(self, access_token: str, base_url: str):
        """

        :param access_token:
        :param base_url:
        """
        self._api_prefix = "api/v2.0"
        self._access_token = access_token
        self._base_url = base_url

    def _get_url(self, sub_path: str) -> str:
        """
        Formats API endpoint absolute URL

        :param sub_path:
        :return:
        """

        path = os.path.join(self._api_prefix, sub_path).lstrip("/")
        return os.path.join(self._base_url, path)

    def _get_headers(self):
        return {"Authorization": f"Token {self._access_token}"}

    def _request(
        self,
        method: types.RequestMethod,
        sub_path: str,
        **kwargs: t.Any,
    ) -> types.AnyResponse:
        """
        Main wrapper for request to the API. Together with required positional arguments
        accepts keyword arguments that are passed to `requests.request` function.

        - json: used to send JSON data with POST, PUT or PATCH request
        - files: send files using multipart/form-urlencoded content type
        - params: send GET query params ({"sort": "date"} will result in ?sort=date)

        :param method: HTTP method name: GET, PUT, POST etc
        :param sub_path: relative to /api/v2.0/ or absolute subpath to the API endpoint.
            Relative subpath should not contain leading backslash: "user-panel/baskets/":
            "http://api.domain.com/api/v2.0/user-panel/baskets/"

            Absolute path must have a leading backslash resulting in URL: "/profile/"
            "http://api.domain.com/profile/"
        :param kwargs:
        :return: JSON response from API if API response code is 200..299. Otherwise,
            raises an exception (a subclass of `push_to_3yourmind.exceptions.BasePushTo3YourmindAPIException`)
        """

        url = self._get_url(sub_path)
        logger.debug(f"Request {method} to {url}")
        response = requests.request(
            method=method,
            url=url,
            headers=self._get_headers(),
            **kwargs,
        )

        if 200 <= response.status_code < 500:
            if response.content:
                response_payload = response.json()
            else:
                response_payload = ""

            if response.status_code == 404:
                raise exceptions.ObjectNotFound(response_payload)
            elif response.status_code == 401:
                raise exceptions.Unauthorized(response_payload)
            elif response.status_code == 400:
                raise exceptions.BadRequest(response_payload)
            elif response.status_code == 405:
                raise exceptions.MethodNotAllowed(response_payload)
            return response_payload
        else:
            raise exceptions.ServerError(response.content)

    @staticmethod
    def _get_parameters(**kwargs) -> t.Dict[str, t.Any]:
        return {
            key: value for key, value in kwargs.items() if value is not types.NoValue
        }
