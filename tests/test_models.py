import ipaddress

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from django_inet.models import (
    ASNField,
    IPAddressField,
    IPNetworkField,
    IPPrefixField,
    MacAddressField,
    URLField,
)

from models import FullModel


def assert_ip_validator(obj):
    """
    assert the validator is set correctly and referring to the correct object
    """
    assert 0 == len(obj.default_validators)
    assert 1 == len(obj.validators)
    assert obj == obj.validators[0].field
    assert obj.version == obj.validators[0].field.version


class ModelTests(TestCase):
    """test model functionality"""

    def test_init(self):
        new0 = URLField()
        new1 = URLField()
        assert 1 == len(new0.default_validators)
        assert 1 == len(new1.default_validators)

        new0 = ASNField()
        new1 = ASNField()
        assert 0 == len(new0.default_validators)
        assert 0 == len(new1.default_validators)

        new0 = IPAddressField()
        new1 = IPAddressField()
        assert_ip_validator(new0)
        assert_ip_validator(new1)

        new0 = IPNetworkField()
        new1 = IPNetworkField()
        assert_ip_validator(new0)
        assert_ip_validator(new1)

        new0 = IPPrefixField()
        new1 = IPPrefixField()
        assert_ip_validator(new0)
        assert_ip_validator(new1)

        new0 = MacAddressField()
        new1 = MacAddressField()
        assert 1 == len(new0.default_validators)
        assert 1 == len(new1.default_validators)

    def test_blank(self):
        model = FullModel()
        model.full_clean()

    def test_asn(self):
        model = FullModel()
        model.asn = 42
        assert 42 == model.asn
        model.full_clean()

        with pytest.raises(ValidationError):
            model.asn = "invalid"
            model.full_clean()

        with pytest.raises(ValidationError):
            model.asn = -1
            model.full_clean()

        model.asn = 4294967295
        model.full_clean()
        assert model.asn == 4294967295

    def test_ipaddress(self):
        model = FullModel()
        model.ip_address = "10.0.0.0"
        assert ipaddress.ip_address("10.0.0.0") == model.ip_address

        with pytest.raises(ValidationError):
            model.ip_address = "invalid"

    def test_ipv4(self):
        model = FullModel()
        model.ipv4 = "10.0.0.0"
        assert ipaddress.ip_address("10.0.0.0") == model.ipv4

        with pytest.raises(ValidationError):
            model.ipv4 = "1::1"

    def test_ipv6(self):
        model = FullModel()
        model.ipv6 = "10::"
        assert ipaddress.ip_address("10::") == model.ipv6

        with pytest.raises(ValidationError):
            model.ipv6 = "10.0.0.0"

    def test_ipnetwork(self):
        model = FullModel()
        model.prefix = "10.0.0.0/8"

        with pytest.raises(ValidationError):
            model.prefix = "invalid"

    def test_mac(self):
        model = FullModel()
        model.mac = "Ff:00:00:12:34:56"
        model.full_clean()
        assert "Ff:00:00:12:34:56" == model.mac

        with pytest.raises(ValidationError):
            model.mac = "invalid"
            model.full_clean()
