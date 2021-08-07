import ipaddress
import warnings

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.core.validators import URLValidator as DjangoURLValidator
from django.db import models
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _


class ConvertOnAssign:
    """
    Calls `field.to_python()` on assign

    """

    def __init__(self, field):
        self.field = field

    def __get__(self, obj, typ=None):
        if obj is None:
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)


class ConvertOnAssignField(models.Field):
    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        setattr(cls, name, ConvertOnAssign(self))


def addr_ctor(version=None):
    if version:
        if version == 4:
            return ipaddress.IPv4Address
        elif version == 6:
            return ipaddress.IPv6Address
        else:
            raise ValueError("unknown version")
    else:
        return ipaddress.ip_address


def prefix_ctor(version=None):
    if version:
        if version == 4:
            return ipaddress.IPv4Network
        elif version == 6:
            return ipaddress.IPv6Network
        else:
            raise ValueError("unknown version")
    else:
        return ipaddress.ip_network


class IPAddressValidator:
    """
    Validates values to be either a v4 or 6 ip address depending
    on the version of the field it is attached to
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        # can't use ctor here because serializer fields don't have it
        wrap_ip_ctor(addr_ctor(self.field.version))(value)


class IPNetworkValidator:
    """
    Validates values to be either a v4 or v6 prefix
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        # can't use ctor here because serializer fields don't have it
        wrap_ip_ctor(prefix_ctor(self.field.version))(value)


class URLValidator(DjangoURLValidator):
    schemes = ["http", "https", "ftp", "ftps", "telnet"]


class URLField(models.URLField):
    default_validators = [URLValidator()]

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "URLField has been deprecated and will be removed in version 1",
            DeprecationWarning,
            stacklevel=2,
        )
        kwargs["max_length"] = 255
        super().__init__(*args, **kwargs)


class ASNField(models.PositiveIntegerField):
    """
    Autonomous System Number
    """

    def __init__(self, **kwargs):

        # append MinValueValidator
        validators = kwargs.get("validators", [])
        validators.append(MinValueValidator(0))
        kwargs.update(validators=validators)

        super().__init__(**kwargs)


def wrap_ip_ctor(ctor):
    def func(value):
        try:
            return ctor(smart_str(value))

        except (ValueError, ipaddress.AddressValueError) as e:
            raise ValidationError(e)

    return func


class IPAddressField(ConvertOnAssignField):
    """
    IP Address
    """

    empty_strings_allowed = True
    max_length = 39
    description = _("IP Address")
    version = None

    def __init__(self, **kwargs):
        kwargs["max_length"] = self.max_length

        self.version = kwargs.pop("version", None)
        self._ctor = wrap_ip_ctor(addr_ctor(self.version))

        super().__init__(**kwargs)

        self.validators.append(IPAddressValidator(self))

    def get_internal_type(self):
        return "CharField"

    def get_prep_value(self, value):
        if value:
            return str(value)
        return None

    def from_db_value(self, value, expression, connection):
        if not value:
            return None
        return self._ctor(value)

    def to_python(self, value):
        if isinstance(value, ipaddress._BaseAddress):
            return value
        if not value:
            return None
        return self._ctor(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return str(value)


class IPNetworkField(ConvertOnAssignField):
    empty_strings_allowed = True
    max_length = 43
    description = _("IP Prefix")
    version = None

    def __init__(self, **kwargs):
        kwargs["max_length"] = self.max_length

        self.version = kwargs.pop("version", None)
        self._ctor = wrap_ip_ctor(prefix_ctor(self.version))

        super().__init__(**kwargs)

        self.validators.append(IPNetworkValidator(self))

    def get_internal_type(self):
        return "CharField"

    def to_python(self, value):
        if isinstance(value, ipaddress._BaseNetwork):
            return value
        if not value:
            return None
        return self._ctor(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return None
        return smart_str(value)

    def value_to_string(self, obj):
        return smart_str(self.value_from_object(obj))


# Alias to original name
IPPrefixField = IPNetworkField


class MacAddressField(ConvertOnAssignField):
    """ """

    empty_strings_allowed = True
    max_length = 17
    description = _("Mac Address")
    default_error_messages = {}
    default_validators = [RegexValidator(r"(?i)^([0-9a-f]{2}[-:]){5}[0-9a-f]{2}$")]

    def __init__(self, **kwargs):
        kwargs["max_length"] = self.max_length
        super().__init__(**kwargs)

    def get_internal_type(self):
        return "CharField"
