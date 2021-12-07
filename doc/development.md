# Development Guide


Structurally client API is a class that is initialized with user's API token and the 
base URL.

```python
from push_to_3yourmind import PushTo3YourmindAPI
client = PushTo3YourmindAPI(access_token="QWERTY123456789", base_url="http://<domain-name>")
```

Functionality is divided into namespaces, for example `my_profile`, `user_panel` etc. 

