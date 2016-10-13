
import ipaddress
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator as DjangoURLValidator
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _


class IPAddressValidator(object):
    """
    Validates values to be either a v4 or 6 ip address depending
    on the version of the field it is attached to
    """
    def __init__(self, field):
        self.field = field
    
    def __call__(self, value):
        try:
            if self.field.version == 4:
                ipaddress.IPv4Address(value)
            elif self.field.version == 6:
                ipaddress.IPv6Address(value)
        except ipaddress.AddressValueError:
            raise ValidationError("Needs to be a valid v%d ip address" % self.field.version)


class IPPrefixValidator(object):
    """
    Validates values to be either a v4 or v6 prefix
    """
    def __init__(self, field):
        self.field = field
    
    def __call__(self, value):
        try:
            if self.field.version == 4:
                ipaddress.IPv4Network(value)
            elif self.field.version == 6:
                ipaddress.IPv6Network(value)
            else:
                try:
                    ipaddress.ip_network(value)
                except ValueError, inst:
                    raise ValidationError(inst)
                    
        except ipaddress.AddressValueError:
            raise ValidationError("Needs to be a valid v%d prefix" % self.field.version)


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


class IPAddressField(models.Field):
    """
    IP Address
    """
    empty_strings_allowed = True
    max_length = 39
    description = _("IP Address")
    default_error_messages = {}
    default_validators = []

    __metaclass__ = models.SubfieldBase
    version = None

# TESTME - doesn't allow blank values
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = self.max_length

        self.default_validators.append(IPAddressValidator(self))

        version = kwargs.pop('version', None)
        if version:
            if version == 4:
                self.__ctor = ipaddress.IPv4Address
            elif version == 6:
                self.__ctor = ipaddress.IPv6Address
            else:
                raise Exception('Unknown version')
        else:
            self.__ctor = ipaddress.ip_address

        super(IPAddressField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def get_prep_value(self, value):
        if value:
            return str(value)
        return None

    def to_python(self, value):
        if isinstance(value, IPAddressField):
            return value
        if not value:
            return None
        return self.__ctor(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return str(value)


# TODO - make errors throw Validation error
class IPPrefixField(models.Field):
    empty_strings_allowed = True
    max_length = 43
    description = _("IP Prefix")
    default_error_messages = {}

    __metaclass__ = models.SubfieldBase
    version = None

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = self.max_length
        if hasattr(kwargs, 'version'):
            if kwargs['version'] == 4:
                self.__ctor = ipaddress.IPv4Network
            elif kwargs['version'] == 6:
                self.__ctor = ipaddress.IPv6Network
            else:
                raise Exception('Unknown version')
        else:
            self.__ctor = ipaddress.ip_network

        super(IPPrefixField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def to_python(self, value):
        if isinstance(value, IPPrefixField):
            return value
        if not value:
            return None
        return self.__ctor(value)

    def get_prep_value(self, value):
        # TODO should validate here?
        value = super(IPPrefixField, self).get_prep_value(value)
        if value is None:
            return None
        return smart_text(value)

    def value_to_string(self, obj):
        return smart_text(self._get_val_from_obj(obj))


class MacAddressField(models.Field):
    empty_strings_allowed = True
    max_length = 17
    description = _("Mac Address")
    default_error_messages = {}

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = self.max_length
        super(MacAddressField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

