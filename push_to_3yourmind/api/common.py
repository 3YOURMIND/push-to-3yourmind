"""
API methods common to all panels.
"""
import typing as t

from push_to_3yourmind import types
from push_to_3yourmind.api.base import BaseAPI


__all__ = ["CommonAPI"]


class CommonAPI(BaseAPI):
    """
    Accessible via namespace `common`, for example:
    >>> response = client.common.get_colors()
    """

    def get_colors(self) -> t.List[types.ResponseDict]:
        return self._request("GET", "colors/")

    def get_units(self) -> t.List[types.ResponseDict]:
        """
        Get list of units of measure available on the platform.
        Currently, "mm" and "inch".
        """
        return self._request("GET", "units/")

    def get_countries(self) -> t.List[types.ResponseDict]:
        """
        Get list of countries with codes and full names
        """
        return self._request("GET", "countries/")

    def get_currencies(self) -> t.List[str]:
        """
        Get list of currencies available on the platform
        """
        return self._request("GET", "currencies/")

    def get_materials(self) -> t.List[types.ResponseDict]:
        return self._request("GET", "materials/")

    # def get_forms(self):
    #     return self._request("GET", "forms/")

    def get_tax_types(self) -> t.List[str]:
        return self._request("GET", "tax-types/")

