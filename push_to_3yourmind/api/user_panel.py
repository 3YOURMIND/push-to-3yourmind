import typing as t
from io import IOBase

from push_to_3yourmind import types, exceptions
from push_to_3yourmind.api.base import BaseAPI
from push_to_3yourmind.types import NoValue


__all__ = ["UserPanelAPI"]


class UserPanelAPI(BaseAPI):
    """
    Groups API functionality from the User Panel, such as creating/updating baskets,
    placing orders, making requests for quotes, ordering quotes etc.
    """

    def get_baskets(
        self,
        *,
        page: types.OptionalNumber = NoValue,
        page_size: types.OptionalNumber = NoValue,
    ) -> t.List[types.ResponseDict]:
        """
        Get all baskets of the current user. Returns paginated list.

        :param page: int, optional
        :param page_size: int, optional
        :return: dictionary with the following keys:
            count: total number of baskets
            currentPage:
            totalPages:
            pageSize: baskets per page
            results: list of basket details
        """

        query = self._get_parameters(page=page, pageSize=page_size)
        return self._request("GET", "user-panel/baskets/", params=query)

    def get_basket(self, *, basket_id: int) -> types.ResponseDict:
        return self._request("GET", f"user-panel/baskets/{basket_id}/")

    def get_basket_price(
        self,
        *,
        basket_id: int,
        currency: str,
        shipping_address_id: types.OptionalNumber = types.NoValue,
        billing_address_id: types.OptionalNumber = types.NoValue,
        shipping_method_id: types.OptionalNumber = types.NoValue,
        voucher_code: types.OptionalString = types.NoValue,
    ) -> types.ResponseDict:
        query = self._get_parameters(
            currency=currency,
            shippingAddressId=shipping_address_id,
            shippingMethodId=shipping_method_id,
            billingAddressId=billing_address_id,
            voucherCode=voucher_code,
        )
        return self._request(
            "GET", f"user-panel/baskets/{basket_id}/price/", params=query
        )

    def create_basket(self) -> types.ResponseDict:
        return self._request("POST", "user-panel/baskets/")

    def delete_basket(self, *, basket_id: int) -> str:
        return self._request("DELETE", f"user-panel/baskets/{basket_id}/")

    def update_basket(
        self, *, basket_id: int, title: types.OptionalNumber = NoValue
    ) -> types.ResponseDict:
        json = self._get_parameters(title=title)
        return self._request("PATCH", f"user-panel/baskets/{basket_id}/", json=json)

    def get_basket_lines(self, *, basket_id: int) -> t.List[types.ResponseDict]:
        return self._request("GET", f"user-panel/baskets/{basket_id}/lines/")

    def get_basket_line(self, *, basket_id: int, line_id) -> types.ResponseDict:
        return self._request("GET", f"user-panel/baskets/{basket_id}/lines/{line_id}/")

    def create_basket_line(self, *, basket_id: int) -> types.ResponseDict:
        return self._request("POST", f"user-panel/baskets/{basket_id}/lines/")

    def upload_cad_file(
        self,
        *,
        basket_id: int,
        unit: types.Unit,
        cad_file: t.Union[str, t.IO],
        line_id: types.OptionalNumber = types.NoValue,
    ) -> types.ResponseDict:

        data = self._get_parameters(basket_id=basket_id, unit=unit, line_id=line_id)
        if isinstance(cad_file, str):
            with open(cad_file, "rb") as cad_file_obj:
                return self._request(
                    "POST", f"/upload/", data=data, files={"file": cad_file_obj}
                )
        elif isinstance(cad_file, IOBase):
            return self._request(
                "POST", f"/upload/", data=data, files={"file": cad_file}
            )
        else:
            raise exceptions.BadArgument(
                "cad_file argument must be either a path to the CAD file "
                "or a file-like object"
            )
