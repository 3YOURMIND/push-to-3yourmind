"""
Groups API functionality from the User Panel, such as creating/updating baskets,
placing orders, making requests for quotes, ordering quotes etc.
"""

import datetime
import decimal
import typing as t
import time

from push_to_3yourmind import types, exceptions, utils
from push_to_3yourmind.logger import logger
from push_to_3yourmind.api.base import BaseAPI
from push_to_3yourmind.types import NoValue


__all__ = ["UserPanelAPI"]


class UserPanelAPI(BaseAPI):
    """
    Accessible via namespace `user_panel`, for example:
    >>> response = client.user_panel.get_baskets()

    Attributes:
        CHECK_FILE_STATUS_MAX_ATTEMPTS: How many times to check for the uploaded CAD file analysis status
        CHECK_FILE_STATUS_DELAY: Delay between status check requests, in seconds
    """

    CHECK_FILE_STATUS_MAX_ATTEMPTS = 120
    CHECK_FILE_STATUS_DELAY = 1.2  # seconds

    def get_baskets(
        self,
        *,
        page: types.OptionalInteger = NoValue,
        page_size: types.OptionalInteger = NoValue,
    ) -> t.List[types.ResponseDict]:
        """
        Get all baskets of the current user. Returns paginated list.

        Args:
            page: int, optional
            page_size: int, optional
        Returns:
            dictionary with the following keys:

            - count: total number of baskets, int
            - currentPage: page number, int
            - totalPages: total number of pages, int
            - pageSize: users per page, int
            - results: list of user details
        """

        query = self._get_parameters(page=page, pageSize=page_size)
        return self._request("GET", "user-panel/baskets/", params=query)

    def get_basket(self, *, basket_id: int) -> types.ResponseDict:
        """
        Args:
            basket_id: int

        Returns:
            Basket details dict
        """
        return self._request("GET", f"user-panel/baskets/{basket_id}/")

    def get_basket_price(
        self,
        *,
        basket_id: int,
        currency: str,
        shipping_address_id: types.OptionalInteger = types.NoValue,
        billing_address_id: types.OptionalInteger = types.NoValue,
        shipping_method_id: types.OptionalInteger = types.NoValue,
        voucher_code: types.OptionalString = types.NoValue,
    ) -> types.ResponseDict:
        """
        Calculate basket's price, given additional optional shipping, billing information

        Args:
            basket_id: int
            currency: str
            shipping_address_id: int, optional
            billing_address_id: int, optional
            shipping_method_id: int, optional
            voucher_code: str, optional

        Returns:
            Dict containing basket prices
        """
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
        self, *, basket_id: int, title: t.Union[str, types.NoValueType] = NoValue
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
        quantity: types.OptionalInteger = types.NoValue,
        product_id: types.OptionalInteger = types.NoValue,
        post_processings: t.Sequence[types.PostProcessingConfig] = (),
        preferred_due_date: types.OptionalDate = types.NoValue,
    ) -> types.ResponseDict:

        if post_processings:
            post_processings = [
                {"postProcessingId": pp.post_processing_id, "colorId": pp.color_id}
                for pp in post_processings
            ]
        if isinstance(preferred_due_date, datetime.date):
            preferred_due_date = preferred_due_date.strftime("%Y-%m-%d")
        json = self._get_parameters(
            quantity=quantity,
            offerId=product_id,
            # postProcessings=post_processings,
            preferredDueDate=preferred_due_date,
        )
        return self._request(
            "PATCH", f"user-panel/baskets/{basket_id}/lines/{line_id}/", json=json
        )

    def add_part_requirements_to_basket_line(
            self,
            *,
            line_id: int,
            form_data: types.FormData,
    ):
        json = {
            "formId": form_data.form_id,
            "fields": [
                {"formFieldId": field.form_field_id, "value": field.value}
                for field in form_data.fields
            ]
        }
        return self._request(
            "POST", f"user-panel/forms/basket-line/{line_id}/",
            json=json,
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
            f"user-panel/baskets/{basket_id}/lines/{line_id}/"
            f"materials/{material_id}/offers/",
            params=query,
        )

    def upload_cad_file_to_basket(
        self,
        *,
        basket_id: int,
        unit: types.Unit,
        cad_file: types.CadFileSpecifier,
        line_id: int,
    ) -> types.ResponseDict:

        data = self._get_parameters(basket_id=basket_id, unit=unit, line_id=line_id)
        cad_file_contents = utils.extract_file_content(cad_file)

        return self._request(
            "POST", f"/upload/", data=data, files={"file": cad_file_contents}
        )

    def upload_cad_file(
        self,
        *,
        unit: types.Unit,
        cad_file: types.CadFileSpecifier,
    ) -> types.ResponseDict:

        data = self._get_parameters(unit=unit)
        cad_file_contents = utils.extract_file_content(cad_file)

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
        # post_processings: t.Sequence[types.PostProcessingConfig] = (),
        preferred_due_date: types.OptionalDate = types.NoValue,
    ) -> types.ResponseDict:
        preferences = self._request("GET", "my-profile/preferences/")
        unit: types.Unit = preferences["unit"]

        line_response = self.create_basket_line(basket_id=basket_id)
        line_id = line_response["id"]
        upload = self.upload_cad_file_to_basket(
            basket_id=basket_id, line_id=line_id, unit=unit, cad_file=cad_file
        )
        self.wait_for_analysis(upload["uuid"])

        return self.update_basket_line(
            basket_id=basket_id,
            line_id=line_id,
            quantity=quantity,
            product_id=product_id,
            # post_processings=post_processings,
            preferred_due_date=preferred_due_date,
        )

    def wait_for_analysis(
        self,
        *,
        file_uuid: str,
    ) -> None:
        max_attempts = self.CHECK_FILE_STATUS_MAX_ATTEMPTS
        for attempt_number in range(max_attempts):
            logger.debug(f"Checking file status {attempt_number}/{max_attempts}")
            response = self._request("GET", f"files/status/{file_uuid}/")
            response_content = response.get("status")
            if response_content == "analysing":
                time.sleep(self.CHECK_FILE_STATUS_DELAY)
                continue
            elif response_content == "finished":
                logger.debug("File analysis done")
                return
            else:
                raise exceptions.FileAnalysisError()

        raise exceptions.FileAnalysisError()

    def create_request_for_quote(
        self, *, basket_id: int, supplier_id: int, message: str
    ) -> types.ResponseDict:
        json = {
            "basketId": basket_id,
            "partnerId": supplier_id,
            "message": message,
        }
        return self._request("POST", f"user-panel/requests-for-quote/", json=json)

    def get_quotes(self) -> types.ResponseDict:
        return self._request("GET", "user-panel/quotes/")

    def get_orders(self) -> types.ResponseDict:
        return self._request("GET", "user-panel/orders/")

    def get_order(self, *, order_id: int) -> types.ResponseDict:
        return self._request("GET", f"user-panel/orders/{order_id}/")

    def get_order_line(self, *, order_id: int, line_id: int) -> types.ResponseDict:
        return self._request("GET", f"user-panel/orders/{order_id}/{line_id}/")

    def get_quote(self, *, quote_id: int) -> types.ResponseDict:
        return self._request("GET", f"user-panel/quotes/{quote_id}/")

    def finalize_quote(
        self,
        *,
        quote_id: int,
        billing_address_id: t.Optional[int] = None,
        shipping_address_id: t.Optional[int] = None,
        shipping_method_id: t.Optional[int] = None,
        pickup_location_id: t.Optional[int] = None,
        delivery_instructions: t.Optional[str] = None,
    ) -> types.ResponseDict:
        json = self._get_parameters(
            billingAddressId=billing_address_id,
            shippingAddressId=shipping_address_id,
            shippingMethodId=shipping_method_id,
            pickupLocationId=pickup_location_id,
            deliveryInstructions=delivery_instructions,
        )
        return self._request(
            "PUT",
            f"user-panel/quotes/{quote_id}/finalize/",
            json=json,
        )

    def place_order_from_quote(
        self,
        *,
        quote_id: int,
        payment_method_id: int,
        authorized_amount: decimal.Decimal,
        reference: t.Optional[str] = None,
        currency: t.Optional[str] = None,
        voucher_code: str = "",
    ) -> types.ResponseDict:
        json = {
            "additionalInformation": {"reference": reference},
            "payment": {
                "currency": currency,
                "details": {},
                "methodId": payment_method_id,
                "authorizedAmount": authorized_amount,
            },
            "quoteId": quote_id,
            "voucherCode": voucher_code,
        }
        return self._request("POST", f"user-panel/orders/", json=json)

    def quick_order_quote(self, *, quote_id: int) -> types.ResponseDict:
        """
        get quote details
        get supplier id

        If quote is not finalized:
           get my addresses, pick one
           get supplier shipping methods, pick one
           finalize quote with one address as shipping and billing,
            one payment method and one shipping method

        get payment methods, pick one
        place order from quote with payment method
        """
        quote_details = self.get_quote(quote_id=quote_id)
        supplier_id = quote_details["partner"]["id"]
        quote_is_finalized = quote_details["status"] == "finalized"

        if not quote_is_finalized:
            addresses = self._request("GET", "my-profile/addresses/")
            address = addresses[0]
            address_id = address["id"]

            shipping_methods = self.get_shipping_methods(
                supplier_id=supplier_id,
                quote_id=quote_id,
                shipping_address_id=address_id,
            )
            shipping_method = shipping_methods[0]
            shipping_method_id = shipping_method["id"]

            self.finalize_quote(
                quote_id=quote_id,
                billing_address_id=address_id,
                shipping_address_id=address_id,
                shipping_method_id=shipping_method_id,
            )
        payment_methods = self.get_payment_methods(supplier_id=supplier_id)
        payment_method = payment_methods[0]
        payment_method_id = payment_method["id"]
        return self.place_order_from_quote(
            quote_id=quote_id,
            payment_method_id=payment_method_id,
            currency=quote_details["currency"],
            authorized_amount=quote_details["totalPrice"]["inclusiveTax"],
        )

    def get_payment_methods(
        self, *, supplier_id: int
    ) -> t.Sequence[types.ResponseDict]:
        return self._request(
            "GET", f"user-panel/services/{supplier_id}/payment-methods/"
        )

    def get_shipping_methods(
        self,
        *,
        supplier_id: int,
        quote_id: types.OptionalInteger = types.NoValue,
        shipping_address_id: types.OptionalInteger = types.NoValue,
    ) -> t.Sequence[types.ResponseDict]:
        query = self._get_parameters(
            quoteId=quote_id, shippingAddressId=shipping_address_id
        )
        return self._request(
            "GET",
            f"user-panel/services/{supplier_id}/shipping-methods/",
            params=query,
        )

    def create_catalog_item_from_basket_line(self, basket_line_id: int) -> types.ResponseDict:
        return self._request(
            "POST",
            "user-panel/catalog/",
            json={"lineId": basket_line_id},
        )

    def upload_catalog_item_attachment(
            self,
            catalog_item_id: int,
            attachment_file: types.AttachmentFileSpecifier,
    ) -> types.ResponseDict:
        attachment_file_contents = utils.extract_file_content(attachment_file)
        return self._request(
            "POST",
            f"user-panel/catalog/{catalog_item_id}/attachments/",
            files={"file": attachment_file_contents},
        )

    def create_catalog_item(
        self,
        detailed_description: t.Optional[str],
        partner_id: t.Optional[int],
        post_processing_product_ids: list[int],
        product_id: int,
        reference: t.Optional[str],
        short_description: t.Optional[str],
        status: t.Literal['published', 'unpublished'],
        stl_file_uuid: str,
        technology_id: int,
        title: str,
    ):
        return self._request(
            "POST",
            "user-panel/catalog/",
            json={
               	"detailedDescription": detailed_description,
                "partnerId": partner_id,
               	"postProcessingProductIds": post_processing_product_ids,
               	"productId": product_id,
               	"reference": reference,
               	"shortDescription": short_description,
               	"status": status,
               	"stlFileUuid": stl_file_uuid,
               	"technologyId": technology_id,
               	"title": title,
            }
        )
