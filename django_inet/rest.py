from rest_framework import serializers

from models import IPAddressValidator, IPPrefixValidator


class IPAddressField(serializers.CharField):
    version = 0
    def __init__(self, **kwargs):
        self.version = kwargs.get("version", 0)
        if "version" in kwargs:
            del kwargs["version"]
        super(IPAddressField, self).__init__(**kwargs)
        self.validators.append(IPAddressValidator(self))


class IPPrefixField(serializers.CharField):
    version = 0
    def __init__(self, **kwargs):
        self.version = kwargs.get("version", 0)
        if "version" in kwargs:
            del kwargs["version"]
        super(IPPrefixField, self).__init__(**kwargs)
        self.validators.append(IPPrefixValidator(self))
