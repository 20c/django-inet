from __future__ import absolute_import
from rest_framework import serializers

from .models import IPAddressValidator, IPPrefixValidator


class IPAddressField(serializers.CharField):
    version = 0
    def __init__(self, **kwargs):
        self.version = kwargs.pop("version", None)
        super(IPAddressField, self).__init__(**kwargs)
        self.validators.append(IPAddressValidator(self))


class IPPrefixField(serializers.CharField):
    version = 0
    def __init__(self, **kwargs):
        self.version = kwargs.pop("version", None)
        super(IPPrefixField, self).__init__(**kwargs)
        self.validators.append(IPPrefixValidator(self))
