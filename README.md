# push-to-3yourmind
A Python SDK library to work with 3YOURMIND's platform API. It enables you to manage user profile
information, push 3D Files, manipulate baskets, lines, get pricing information, place Orders 
and Catalog Items.

# Usage Guide

[link](./docs/push_to_3yourmind/index.md)

## Requirements

Python >= 3.6

## Create access token for your user

All operations 

Open `/admin/auth/user/`, and click "Create token" in the user list.

## Installation

    pip install -e git+https://github.com/3YOURMIND/push-to-3yourmind.git#egg=push_to_3yourmind

## Usage

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

# get current user's basket list
baskets = client.user_panel.get_baskets()
# or 
basket = client.user_panel.get_basket(basket_id=6)

```

# Library Development Guide

[link](./doc/development.md)

# @

Copyright 3YOURMIND GmbH
