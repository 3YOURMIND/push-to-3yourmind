Module push_to_3yourmind.api.common
===================================

Classes
-------

`CommonAPI(access_token: str, base_url: str)`
:   Base class for all namespaced API methods.
    
    :param access_token:
    :param base_url:

    ### Methods

    `get_colors(self) ‑> List[Dict[str, Any]]`
    :

    `get_units(self) ‑> List[Dict[str, Any]]`
    :   Get list of units of measure available on the platform.
        Currently, "mm" and "inch".
        :return:

    `get_countries(self) ‑> List[Dict[str, Any]]`
    :   Get list of countries with codes and full names
        :return:

    `get_currencies(self) ‑> List[str]`
    :   Get list of currencies available on the platform
        :return:

    `get_materials(self) ‑> List[Dict[str, Any]]`
    :

    `get_tax_types(self) ‑> List[str]`
    :