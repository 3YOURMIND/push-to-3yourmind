import typing as t

from push_to_3yourmind import types
from push_to_3yourmind.api.base import BaseAPI


__all__ = ["MyProfileAPI"]


class MyProfileAPI(BaseAPI):
    def get_preferences(self) -> types.ResponseDict:
        """
        Get preferences of the current user: country, currency, language, unit
        """

        return self._request("GET", "my-profile/preferences/")

    def set_preferences(
        self,
        *,
        country: types.OptionalString = types.NoValue,
        currency: types.OptionalString = types.NoValue,
        language: types.OptionalString = types.NoValue,
        unit: types.OptionalString = types.NoValue,
    ) -> types.ResponseDict:
        """
        Update profile of the current user. All arguments are optional, only passed
        values will be saved to the profile.

        Args:
            country: 2-letter country code, ex. US, FR, GB
            currency: 3-letter currency code, ex. USD, EUR
            language: 2-letter language code, ex. en, de, fr, es
            unit: mm or inch
        """

        json = self._get_parameters(
            country=country, currency=currency, language=language, unit=unit
        )
        return self._request("PUT", "my-profile/preferences/", json=json)

    def get_profile(self) -> types.ResponseDict:
        """
        Get profile of the current user: name, default address, access roles etc.
        """

        return self._request("GET", "my-profile/profile/")

    def get_addresses(self) -> t.List[types.ResponseDict]:
        """
        Get a list of current user's addresses
        """

        return self._request("GET", "my-profile/addresses/")

    def get_address(self, *, address_id: int) -> types.ResponseDict:
        """
        Get specific address of the current user
        """

        return self._request("GET", f"my-profile/addresses/{address_id}/")
