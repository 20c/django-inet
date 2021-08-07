from django.db import models

from django_inet.models import (
    ASNField,
    IPAddressField,
    IPNetworkField,
    MacAddressField,
    URLField,
)


class FullModel(models.Model):
    url = URLField(null=True, blank=True)
    asn = ASNField(null=True, blank=True)
    ipv4 = IPAddressField(version=4, null=True, blank=True)
    ipv6 = IPAddressField(version=6, null=True, blank=True)
    ip_address = IPAddressField(null=True, blank=True)

    prefix = IPNetworkField(null=True, blank=True)
    prefix4 = IPNetworkField(version=4, null=True, blank=True)
    prefix6 = IPNetworkField(version=6, null=True, blank=True)
    mac = MacAddressField(null=True, blank=True)

    class Meta:
        app_label = "django_inet.tests"
