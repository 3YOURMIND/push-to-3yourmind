from push_to_3yourmind.api.base import BaseAPI
from push_to_3yourmind.api.common import CommonAPI
from push_to_3yourmind.api.my_profile import MyProfileAPI
from push_to_3yourmind.api.user_panel import UserPanelAPI


__all__ = ["PushTo3YourmindAPI"]


class PushTo3YourmindAPI(BaseAPI):
    def __init__(self, access_token: str, base_url: str):
        super().__init__(access_token, base_url)
        self.user_panel = UserPanelAPI(access_token, base_url)
        self.common = CommonAPI(access_token, base_url)
        self.my_profile = MyProfileAPI(access_token, base_url)
