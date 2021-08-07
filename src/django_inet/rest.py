from rest_framework import serializers

from .models import IPAddressValidator, IPNetworkValidator


class IPAddressField(serializers.CharField):
    version = 0

    def __init__(self, **kwargs):
        self.version = kwargs.pop("version", None)
        super().__init__(**kwargs)
        self.validators.append(IPAddressValidator(self))


class IPNetworkField(serializers.CharField):
    version = 0

    def __init__(self, **kwargs):
        self.version = kwargs.pop("version", None)
        super().__init__(**kwargs)
        self.validators.append(IPNetworkValidator(self))
