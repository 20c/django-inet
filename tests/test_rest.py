
import pytest
import unittest
from rest_framework import serializers

from django_inet.rest import (
    IPAddressField,
    IPPrefixField
)

class InetSerializer(serializers.Serializer):
    ip = IPAddressField()
    ip4 = IPAddressField(version=4)
    ip6 = IPAddressField(version=6)
    prefix = IPPrefixField()
    prefix4 = IPPrefixField(version=4)
    prefix6 = IPPrefixField(version=6)

class RestTestCase(unittest.TestCase):
    def test_validation(self):

        # test valid addresses and prefixes (no errors expected)
        slz = InetSerializer(data={
            'ip' : '192.168.1.1',
            'ip4' : '192.168.1.1',
            'ip6' : 'fe80::1',
            'prefix' : '192.168.0.0/23',
            'prefix4' : '192.168.0.0/23',
            'prefix6' : '2001:0db8:35a3:0000::/64'
        })
        if not slz.is_valid():
            print(slz.errors)
        assert slz.is_valid()

        # test invalid addresses and prefixes (errors expected)
        data={
            'ip': 'invalid',
            'ip4': 'fe80::1',
            'ip6': '10.0.0.0',
            'prefix': 'invalid',
            'prefix4': 'fe80::/10',
            'prefix6': '192.168.0.0/23',
        }
        slz = InetSerializer(data=data)
        assert not slz.is_valid()
        self.assertEqual(slz.is_valid(), False)
        errors = slz.errors
        assert data.keys() == errors.keys()
