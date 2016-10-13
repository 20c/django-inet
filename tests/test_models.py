
from django.test import TestCase
import pytest

from django_inet.models import (
    URLField,
    ASNField,
    IPAddressField,
    IPPrefixField,
    MacAddressField,
)


class ModelTests(TestCase):
    """ test model functionality """

    def test_init(self):
        new = URLField()
        new = ASNField()
        new = IPAddressField()
        new = IPPrefixField()
        new = MacAddressField()

