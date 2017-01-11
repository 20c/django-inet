
import ipaddress
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator as DjangoURLValidator
from django.core.validators import RegexValidator
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _


class ConvertOnAssign(object):
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
        super(ConvertOnAssignField, self).contribute_to_class(cls, name)
        setattr(cls, name, ConvertOnAssign(self))


class IPAddressValidator(object):
    """
    Validates values to be either a v4 or 6 ip address depending
    on the version of the field it is attached to
    """
    def __init__(self, field):
        self.field = field
    
    def __call__(self, value):
        self.field._ctor(value)


class IPPrefixValidator(object):
    """
    Validates values to be either a v4 or v6 prefix
    """
    def __init__(self, field):
        self.field = field
    
    def __call__(self, value):
        self.field._ctor(value)


class URLValidator(DjangoURLValidator):
    schemes = ["http", "https", "ftp", "ftps", "telnet"]


class URLField(models.URLField):
    default_validators = [URLValidator()]

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 255
        super(URLField, self).__init__(*args, **kwargs)


class ASNField(models.PositiveIntegerField):
    """
    Autonomous System Number
    """
    def __init__(self, *args, **kwargs):
        super(ASNField, self).__init__(*args, **kwargs)


def wrap_ip_ctor(ctor):
    def func(value):
        try:
            return ctor(smart_text(value))

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
    default_error_messages = {}
    default_validators = []
    version = None

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = self.max_length

        self.default_validators.append(IPAddressValidator(self))

        version = kwargs.pop('version', None)
        if version:
            if version == 4:
                self._ctor = wrap_ip_ctor(ipaddress.IPv4Address)
            elif version == 6:
                self._ctor = wrap_ip_ctor(ipaddress.IPv6Address)
            else:
                raise Exception('Unknown version')
        else:
            self._ctor = wrap_ip_ctor(ipaddress.ip_address)

        super(IPAddressField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def get_prep_value(self, value):
        if value:
            return str(value)
        return None

    def from_db_value(self, value, expression, connection, context):
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
        value = self._get_val_from_obj(obj)
        return str(value)


class IPPrefixField(ConvertOnAssignField):
    empty_strings_allowed = True
    max_length = 43
    description = _("IP Prefix")
    default_error_messages = {}
    version = None

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = self.max_length

        version = kwargs.pop('version', None)
        if version:
            if version == 4:
                self._ctor = wrap_ip_ctor(ipaddress.IPv4Network)
            elif version == 6:
                self._ctor = wrap_ip_ctor(ipaddress.IPv6Network)
            else:
                raise Exception('Unknown version')
        else:
            self._ctor = wrap_ip_ctor(ipaddress.ip_network)

        super(IPPrefixField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def to_python(self, value):
        if isinstance(value, ipaddress._BaseNetwork):
            return value
        if not value:
            return None
        return self._ctor(value)

    def get_prep_value(self, value):
        value = super(IPPrefixField, self).get_prep_value(value)
        if value is None:
            return None
        return smart_text(value)

    def value_to_string(self, obj):
        return smart_text(self._get_val_from_obj(obj))


class MacAddressField(ConvertOnAssignField):
    """
    """
    empty_strings_allowed = True
    max_length = 17
    description = _("Mac Address")
    default_error_messages = {}
    default_validators = []

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = self.max_length
        super(MacAddressField, self).__init__(*args, **kwargs)

        self.default_validators.append(
            RegexValidator(r'(?i)^([0-9a-f]{2}[-:]){5}[0-9a-f]{2}$')
        )

    def get_internal_type(self):
        return "CharField"

