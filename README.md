# push-to-3yourmind
This is a python library that enables you to push 3D Files, Orders and Catalog Items to the 3YOURMIND Software.

# Usage Guide

```python
from push_to_3yourmind import PushTo3YourmindAPI
client = PushTo3YourmindAPI(
    access_token="QWERTY123456789", 
    base_url="http://<domain-name>",
)

profile_info = client.my_profile.get_profile()
my_preferences = client.my_profile.get_preferences()
client.my_profile.set_preferences(currency="USD", language="de")
# or
client.my_profile.set_preferences(language="en")
# or
client.my_profile.set_preferences(unit="inch")

baskets = client.user_panel.get_baskets()
# or 
basket = client.user_panel.get_basket(basket_id=6)

```
