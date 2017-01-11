
from django.core.exceptions import ValidationError
from django.test import TestCase
import ipaddress
import pytest

from django_inet.models import (
    URLField,
    ASNField,
    IPAddressField,
    IPPrefixField,
    MacAddressField,
)
from models import FullModel


class ModelTests(TestCase):
    """ test model functionality """

    def test_init(self):
        new = URLField()
        new = ASNField()
        new = IPAddressField()
        new = IPPrefixField()
        new = MacAddressField()

    def test_blank(self):
        model = FullModel()
        model.full_clean()

    def test_asn(self):
        model = FullModel()
        model.asn = 42
        assert 42 == model.asn

        with pytest.raises(ValidationError):
            model.asn = 'invalid'
            model.full_clean()

    def test_ipaddress(self):
        model = FullModel()
        model.ip_address = '10.0.0.0'
        assert ipaddress.ip_address(u'10.0.0.0') == model.ip_address

        with pytest.raises(ValidationError):
            model.ip_address = 'invalid'

    def test_ipv4(self):
        model = FullModel()
        model.ipv4 = '10.0.0.0'
        assert ipaddress.ip_address(u'10.0.0.0') == model.ipv4

        with pytest.raises(ValidationError):
            model.ipv4 = '1::1'

    def test_ipv6(self):
        model = FullModel()
        model.ipv6 = '10::'
        assert ipaddress.ip_address(u'10::') == model.ipv6

        with pytest.raises(ValidationError):
            model.ipv6 = '10.0.0.0'

    def test_ipprefix(self):
        model = FullModel()
        model.prefix = '10.0.0.0/8'

        with pytest.raises(ValidationError):
            model.prefix = 'invalid'

    def test_mac(self):
        model = FullModel()
        model.mac = 'Ff:00:00:12:34:56'
        model.full_clean()
        assert 'Ff:00:00:12:34:56' == model.mac

        with pytest.raises(ValidationError):
            model.mac = 'invalid'
            model.full_clean()

