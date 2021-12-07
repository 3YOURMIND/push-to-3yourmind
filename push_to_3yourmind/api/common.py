import typing as t

from push_to_3yourmind import types
from push_to_3yourmind.api.base import BaseAPI


__all__ = ["CommonAPI"]


class CommonAPI(BaseAPI):
    def get_colors(self) -> t.List[types.ResponseDict]:
        return self._request("GET", "colors/")

    def get_units(self) -> t.List[types.ResponseDict]:
        return self._request("GET", "units/")

    def get_countries(self) -> t.List[types.ResponseDict]:
        return self._request("GET", "countries/")

    def get_currencies(self) -> t.List[str]:
        return self._request("GET", "currencies/")

    def get_materials(self) -> t.List[types.ResponseDict]:
        return self._request("GET", "materials/")

    def get_tax_types(self) -> t.List[str]:
        return self._request("GET", "tax-types/")

