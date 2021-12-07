import os
import typing as t

import requests

from push_to_3yourmind import exceptions
from push_to_3yourmind import types
from push_to_3yourmind.logger import logger


__all__ = ["BaseAPI"]


class BaseAPI:
    def __init__(self, access_token: str, base_url: str):
        self._api_prefix = "api/v2.0"
        self._access_token = access_token
        self._base_url = base_url

    def _get_url(self, sub_path: str) -> str:
        path = os.path.join(self._api_prefix, sub_path).lstrip("/")
        return os.path.join(self._base_url, path)

    def _request(
        self,
        method: types.RequestMethod,
        sub_path: str,
        **kwargs: t.Any,
    ) -> types.AnyResponse:
        url = self._get_url(sub_path)
        logger.debug(f"Request {method} to {url}")
        response = requests.request(
            method=method,
            url=url,
            headers={"Authorization": f"Token {self._access_token}"},
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
