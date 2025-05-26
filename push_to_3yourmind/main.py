"""
Main class/entrypoint declaration
"""
from push_to_3yourmind.api.base import BaseAPI
from push_to_3yourmind.api.common import CommonAPI
from push_to_3yourmind.api.my_profile import MyProfileAPI
from push_to_3yourmind.api.organization_panel import OrganizationPanelAPI
from push_to_3yourmind.api.user_panel import UserPanelAPI


__all__ = ["PushTo3YourmindAPI"]


class PushTo3YourmindAPI(BaseAPI):
    """
    The main class and the entrypoint for API

    >>> from push_to_3yourmind import PushTo3YourmindAPI
    >>> client = PushTo3YourmindAPI(access_token="QWERTY123456789", base_url="http://<domain-name>")

    Functionality is divided into namespaces, for example `my_profile`, `user_panel` etc. Some
    API endpoints require proper user permissions, in case when an API can't be reached, an exception
    AccessDenied is raised.

    Attributes:
        user_panel: order management-related API: create/update basket lines,
            upload CAD files, pricing
        common: common API: country, unit, material lists
        my_profile: API to manage user's preferences, profile, address list etc
    """

    def __init__(self, access_token: str, base_url: str):
        super().__init__(access_token, base_url)
        self.user_panel = UserPanelAPI(access_token, base_url)
        self.common = CommonAPI(access_token, base_url)
        self.my_profile = MyProfileAPI(access_token, base_url)
        self.organization_panel = OrganizationPanelAPI(access_token, base_url)
