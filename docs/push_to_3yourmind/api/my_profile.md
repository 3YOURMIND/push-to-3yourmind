Module push_to_3yourmind.api.my_profile
=======================================

Classes
-------

`MyProfileAPI(access_token: str, base_url: str)`
:   Base class for all namespaced API methods.
    
    :param access_token:
    :param base_url:

    ### Methods

    `get_preferences(self) ‑> Dict[str, Any]`
    :   Get preferences of the current user: country, currency, language, unit
        
        :return:

    `set_preferences(self, *, country: Union[str, bytes, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue, currency: Union[str, bytes, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue, language: Union[str, bytes, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue, unit: Union[str, bytes, Type[push_to_3yourmind.types.NoValue]] = push_to_3yourmind.types.NoValue) ‑> Dict[str, Any]`
    :   Update profile of the current user. All arguments are optional, only passed
        values will be saved to the profile.
        
        :param country: 2-letter country code, ex. US, FR, GB
        :param currency: 3-letter currency code, ex. USD, EUR
        :param language: 2-letter language code, ex. en, de, fr, es
        :param unit: mm or inch
        :return:

    `get_profile(self) ‑> Dict[str, Any]`
    :   Get profile of the current user: name, default address, access roles etc.
        
        :return:

    `get_addresses(self) ‑> List[Dict[str, Any]]`
    :   Get a list of current user's addresses
        
        :return:

    `get_address(self, *, address_id: int) ‑> Dict[str, Any]`
    :   Get specific address of the current user
        
        :return: