import typing as t

from push_to_3yourmind import types
from push_to_3yourmind.api.base import BaseAPI


__all__ = ["MyProfileAPI"]


class MyProfileAPI(BaseAPI):
    def get_preferences(self) -> types.ResponseDict:
        return self._request("GET", "my-profile/preferences/")

    def set_preferences(
        self,
        *,
        country: types.OptionalString = types.NoValue,
        currency: types.OptionalString = types.NoValue,
        language: types.OptionalString = types.NoValue,
        unit: types.OptionalString = types.NoValue,
    ) -> types.ResponseDict:
        json = self._get_parameters(
            country=country, currency=currency, language=language, unit=unit
        )
        return self._request("PUT", "my-profile/preferences/", json=json)

    def get_profile(self) -> types.ResponseDict:
        return self._request("GET", "my-profile/profile/")

    def get_addresses(self) -> t.List[types.ResponseDict]:
        return self._request("GET", "my-profile/addresses/")

    def get_address(self, *, address_id: int) -> types.ResponseDict:
        return self._request("GET", f"my-profile/addresses/{address_id}/")
