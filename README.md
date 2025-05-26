# push-to-3yourmind

A Python SDK library to work with 3YOURMIND's platform API. It enables you to manage user profile
information, push 3D Files, manipulate baskets, lines, get pricing information, place Orders
and Catalog Items.

# Quickstart

## Requirements

Python >= 3.12

## Create access token for your user

Open `/admin/auth/user/`, and click "Create token" in the user list.

## Installation

    pip install -e git+https://github.com/3YOURMIND/push-to-3yourmind.git#egg=push_to_3yourmind

## Usage

### First, initialize API class

```python
from push_to_3yourmind import PushTo3YourmindAPI
client = PushTo3YourmindAPI(
    access_token="QWERTY123456789",
    base_url="http://<domain-name>",
)
```

### Get or set current user's info

```python
profile_info = client.my_profile.get_profile()
my_preferences = client.my_profile.get_preferences()
client.my_profile.set_preferences(currency="USD", language="de")
# or
client.my_profile.set_preferences(language="en")
# or
client.my_profile.set_preferences(unit="inch")
```

### Explore User Panel's API

```python
# get current user's basket list
baskets = client.user_panel.get_baskets()
# or
basket = client.user_panel.get_basket(basket_id=6)
```

### Do more with a single API call

```python
client.user_panel.create_line_with_cad_file_and_product(
    basket_id=4,
    cad_file="/path/to/the/cad_file.stl",
    product_id=3,
    quantity=1,
)
```

# Usage Guide

[Creating a basket, placing an order](https://3yourmind.github.io/push-to-3yourmind/api/user_panel.html)

[User profile management](https://3yourmind.github.io/push-to-3yourmind/api/my_profile.html)

[Common API](https://3yourmind.github.io/push-to-3yourmind/api/common.html)

[there is more](https://3yourmind.github.io/push-to-3yourmind/)

# Documentation generation

    poetry install
    poetry shell
    make documentation

# @

Copyright 3YOURMIND GmbH
