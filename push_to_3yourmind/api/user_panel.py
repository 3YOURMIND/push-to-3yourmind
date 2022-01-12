import typing as t
from io import IOBase, BytesIO

import requests

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

    def delete_basket(self, basket_id: int) -> str:
        return self._request("DELETE", f"user-panel/baskets/{basket_id}/")

    def update_basket(
        self, *, basket_id: int, title: types.OptionalNumber = NoValue
    ) -> types.ResponseDict:
        json = self._get_parameters(title=title)
        return self._request("PATCH", f"user-panel/baskets/{basket_id}/", json=json)

    def get_basket_lines(self, basket_id: int) -> t.List[types.ResponseDict]:
        return self._request("GET", f"user-panel/baskets/{basket_id}/lines/")

    def get_basket_line(self, *, basket_id: int, line_id) -> types.ResponseDict:
        return self._request("GET", f"user-panel/baskets/{basket_id}/lines/{line_id}/")

    def create_basket_line(self, basket_id: int) -> types.ResponseDict:
        return self._request("POST", f"user-panel/baskets/{basket_id}/lines/")

    def update_basket_line(
        self,
        *,
        basket_id: int,
        line_id: int,
        quantity: types.OptionalNumber = types.NoValue,
        product_id: types.OptionalNumber = types.NoValue,
        post_processing_ids: types.OptionalNumberSequence = (),
    ) -> types.ResponseDict:

        post_processings = [
            {"postProcessingId": post_processing_id}
            for post_processing_id in post_processing_ids
        ]

        json = self._get_parameters(
            quantity=quantity, offerId=product_id, postProcessings=post_processings
        )
        return self._request(
            "PATCH", f"user-panel/baskets/{basket_id}/lines/{line_id}/", json=json
        )

    def get_materials(
        self, *, basket_id: int, line_id: int
    ) -> t.List[types.ResponseDict]:
        preferences = self._request("GET", "my-profile/preferences/")
        country = preferences["country"]
        query = {"country": country}

        return self._request(
            "GET",
            f"user-panel/baskets/{basket_id}/lines/{line_id}/materials/",
            params=query,
        )

    def get_products(
        self, *, basket_id: int, line_id: int, material_id: int
    ) -> t.List[types.ResponseDict]:
        preferences = self._request("GET", "my-profile/preferences/")
        country = preferences["country"]
        query = {"country": country}

        return self._request(
            "GET",
            f"user-panel/baskets/{basket_id}/lines/{line_id}/materials/{material_id}/offers/",
            params=query,
        )

    def upload_cad_file(
        self,
        *,
        basket_id: int,
        unit: types.Unit,
        cad_file: types.CadFileSpecifier,
        line_id: types.OptionalNumber = types.NoValue,
    ) -> types.ResponseDict:

        data = self._get_parameters(basket_id=basket_id, unit=unit, line_id=line_id)
        if isinstance(cad_file, str):
            if cad_file.startswith("http"):
                response = requests.get(cad_file)
                cad_file_contents = BytesIO(response.content)
            else:
                with open(cad_file, "rb") as cad_file_obj:
                    cad_file_contents = BytesIO(cad_file_obj.read())
        elif isinstance(cad_file, IOBase):
            cad_file_contents = cad_file

        else:
            raise exceptions.BadArgument(
                "cad_file argument must be either a path to the CAD file "
                "or a file-like object"
            )

        return self._request(
            "POST", f"/upload/", data=data, files={"file": cad_file_contents}
        )


    def create_line_with_cad_file_and_product(
        self,
        *,
        basket_id: int,
        cad_file: types.CadFileSpecifier,
        product_id: int,
        quantity: int,
        post_processing_ids: t.Sequence[int] = (),
    ) -> types.ResponseDict:
        preferences = self._request("GET", "my-profile/preferences/")
        unit = preferences["unit"]

        line_response = self.create_basket_line(basket_id=basket_id)
        line_id = line_response["id"]
        self.upload_cad_file(
            basket_id=basket_id, line_id=line_id, unit=unit, cad_file=cad_file
        )

        return self.update_basket_line(
            basket_id=basket_id,
            line_id=line_id,
            quantity=quantity,
            product_id=product_id,
            post_processing_ids=post_processing_ids,
        )

    def create_request_for_quote(
        self, *, basket_id: int, supplier_id: int, message: str
    ) -> types.ResponseDict:
        json = {
            "basketId": basket_id,
            "partnerId": supplier_id,
            "message": message,
        }
        return self._request("POST", f"user-panel/requests-for-quote/", json=json)
