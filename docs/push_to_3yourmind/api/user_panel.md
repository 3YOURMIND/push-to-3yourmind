Module push_to_3yourmind.api.user_panel
=======================================

Classes
-------

`UserPanelAPI(access_token: str, base_url: str)`
:   Groups API functionality from the User Panel, such as creating/updating baskets,
    placing orders, making requests for quotes, ordering quotes etc.
    
    :param access_token:
    :param base_url:

    ### Class variables

    `CHECK_FILE_STATUS_MAX_ATTEMPTS`
    :

    `CHECK_FILE_STATUS_DELAY`
    :

    ### Methods

    `get_baskets(self, *, page: Union[int, float, decimal.Decimal, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue, page_size: Union[int, float, decimal.Decimal, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue) ‑> List[Dict[str, Any]]`
    :   Get all baskets of the current user. Returns paginated list.
        
        :param page: int, optional
        :param page_size: int, optional
        :return: dictionary with the following keys:
            count: total number of baskets
            currentPage:
            totalPages:
            pageSize: baskets per page
            results: list of basket details

    `get_basket(self, *, basket_id: int) ‑> Dict[str, Any]`
    :

    `get_basket_price(self, *, basket_id: int, currency: str, shipping_address_id: Union[int, float, decimal.Decimal, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue, billing_address_id: Union[int, float, decimal.Decimal, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue, shipping_method_id: Union[int, float, decimal.Decimal, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue, voucher_code: Union[str, bytes, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue) ‑> Dict[str, Any]`
    :

    `create_basket(self) ‑> Dict[str, Any]`
    :

    `delete_basket(self, basket_id: int) ‑> str`
    :

    `update_basket(self, *, basket_id: int, title: Union[int, float, decimal.Decimal, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue) ‑> Dict[str, Any]`
    :

    `get_basket_lines(self, basket_id: int) ‑> List[Dict[str, Any]]`
    :

    `get_basket_line(self, *, basket_id: int, line_id) ‑> Dict[str, Any]`
    :

    `create_basket_line(self, basket_id: int) ‑> Dict[str, Any]`
    :

    `update_basket_line(self, *, basket_id: int, line_id: int, quantity: Union[int, float, decimal.Decimal, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue, product_id: Union[int, float, decimal.Decimal, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue, post_processing_ids: Sequence[Union[int, float, decimal.Decimal, Type[push_to_3yourmind.types.NoValue]]] = (), preferred_due_date: Union[datetime.date, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue) ‑> Dict[str, Any]`
    :

    `get_materials(self, *, basket_id: int, line_id: int) ‑> List[Dict[str, Any]]`
    :

    `get_products(self, *, basket_id: int, line_id: int, material_id: int) ‑> List[Dict[str, Any]]`
    :

    `upload_cad_file(self, *, basket_id: int, unit: Literal['mm', 'inch'], cad_file: Union[str, IO], line_id: int) ‑> Dict[str, Any]`
    :

    `create_line_with_cad_file_and_product(self, *, basket_id: int, cad_file: Union[str, IO], product_id: int, quantity: int, post_processing_ids: Sequence[int] = (), preferred_due_date: Union[datetime.date, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue) ‑> Dict[str, Any]`
    :

    `check_uploaded_file_status(self, *, basket_id: int, line_id: int) ‑> None`
    :

    `create_request_for_quote(self, *, basket_id: int, supplier_id: int, message: str) ‑> Dict[str, Any]`
    :

    `get_quotes(self) ‑> Dict[str, Any]`
    :

    `get_orders(self) ‑> Dict[str, Any]`
    :

    `get_order(self, *, order_id: int) ‑> Dict[str, Any]`
    :

    `get_order_line(self, *, order_id: int, line_id: int) ‑> Dict[str, Any]`
    :

    `get_quote(self, *, quote_id: int) ‑> Dict[str, Any]`
    :

    `finalize_quote(self, *, quote_id: int, billing_address_id: Optional[int] = None, shipping_address_id: Optional[int] = None, shipping_method_id: Optional[int] = None, pickup_location_id: Optional[int] = None, delivery_instructions: Optional[str] = None) ‑> Dict[str, Any]`
    :

    `place_order_from_quote(self, *, quote_id: int, payment_method_id: int, authorized_amount: decimal.Decimal, reference: Optional[str] = None, currency: Optional[str] = None, voucher_code: str = '') ‑> Dict[str, Any]`
    :

    `quick_order_quote(self, *, quote_id: int) ‑> Dict[str, Any]`
    :   get quote details
        get supplier id
        
        If quote is not finalized:
           get my addresses, pick one
           get supplier shipping methods, pick one
           finalize quote with one address as shipping and billing,
            one payment method and one shipping method
        
        get payment methods, pick one
        place order from quote with payment method

    `get_payment_methods(self, *, supplier_id: int) ‑> Sequence[Dict[str, Any]]`
    :

    `get_shipping_methods(self, *, supplier_id: int, quote_id: Union[int, float, decimal.Decimal, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue, shipping_address_id: Union[int, float, decimal.Decimal, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue) ‑> Sequence[Dict[str, Any]]`
    :