
# django-inet

[![PyPI](https://img.shields.io/pypi/v/django-inet.svg?maxAge=3600)](https://pypi.python.org/pypi/django-inet)
[![PyPI](https://img.shields.io/pypi/pyversions/django-inet.svg)](https://pypi.python.org/pypi/django-inet)
[![Tests](https://github.com/20c/django-inet/workflows/tests/badge.svg)](https://github.com/20c/django-inet)
[![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/20c/django-inet)](https://lgtm.com/projects/g/20c/django-inet/alerts/)
[![Codecov](https://img.shields.io/codecov/c/github/20c/django-inet/master.svg?maxAge=3600)](https://codecov.io/github/20c/django-inet)


django internet utilities


## Provides

```py
ASNField()
IPAddressField(version=None)
IPNetworkField(version=None)
MacAddressField()
```

`IPPrefixField` has been renamed to `IPNetworkField` to conform with other python package names (like `ipaddress`).

Addresses and Prefixes are stored and strings and converted to ipaddress.IPv{4,6}{Address,Prefix} classes.

Version can be set to 4 or 6 to force a version, or left as None to use
either.

## Quickstart

Install django-inet

```sh
pip install django-inet
```

Then use it in a project

```py
import django_inet
```


## License

Copyright 2014-2021 20C, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this software except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.