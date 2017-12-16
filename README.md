
# django-inet

[![PyPI](https://img.shields.io/pypi/v/django-inet.svg?maxAge=3600)](https://pypi.python.org/pypi/django-inet)
[![PyPI](https://img.shields.io/pypi/pyversions/django-inet.svg)](https://pypi.python.org/pypi/django-inet)
[![Travis CI](https://img.shields.io/travis/20c/django-inet.svg?maxAge=3600)](https://travis-ci.org/20c/django-inet)
[![Code Health](https://landscape.io/github/20c/django-inet/master/landscape.svg?style=flat)](https://landscape.io/github/20c/django-inet/master)
[![Codecov](https://img.shields.io/codecov/c/github/20c/django-inet/master.svg?maxAge=3600)](https://codecov.io/github/20c/django-inet)
[![Requires.io](https://img.shields.io/requires/github/20c/django-inet.svg?maxAge=3600)](https://requires.io/github/20c/django-inet/requirements)

django internet utilities


## Provides

```py
ASNField()
IPAddressField(version=None)
IPPrefixField(version=None)
```

Addresses and Prefixes are stored and strings and converted to ipaddress.IPv{4,6}{Address,Prefix} classes.

Version can be set to 4 or 6 to force a version, or left as None to use
either.

Tested in python 2.7, 3.3, 3.4, 3.5 and django 1.8, 1.9, 1.10


## Quickstart

Install django-inet

```sh
pip install django-inet
```

Then use it in a project

```py
import django_inet
```



### License

Copyright 2014 20C, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this softare except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

