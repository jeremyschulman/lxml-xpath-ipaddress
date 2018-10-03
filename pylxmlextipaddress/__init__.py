"""
MIT License

Copyright (c) 2018 Jeremy Schulman

This module defines an LXML extension library that wraps the ipaddress python module.

Examples
--------

from lxml import etree
import pylxmlextipaddress

# given "config" is an LXML XML structure, you can run the XPath to find all IPv4 network items:

config = etree.parse('tests/config.xml').getroot()

ns = {'ip': pylxmlextipaddress.NAMESPACE}

items = config.xpath('//*[ip:is-net-ip4(.)', namespaces=ns)

print(items[0].text)
>>> 10.10.0.0/16
"""

from lxml.etree import FunctionNamespace
import ipaddress
from functools import wraps

NAMESPACE = 'http://pylxmlipaddress.jeremyschulman.com'

# register this namespace into the lxml system
# the caller must use the NAMESPACE value when calling xpath with the namespace= argument

_ns_ext = FunctionNamespace(NAMESPACE)


# ----------------------------------------------------------------------------
# IPv4 functions
# ----------------------------------------------------------------------------

def is_any_ip4(value):
    """
    Determine if this given value is an IPv4 address, an IPv4 network value, or an IPv4 interface value;
    as defined by the ipaddress module

    Parameters
    ----------
    value : str
        The value to check

    Returns
    -------
    bool
        True if the value is any valid IPv4 thing
        False otherwise
    """
    for test in [ipaddress.IPv4Network, ipaddress.IPv4Interface, ipaddress.IPv4Address]:
        try:
            return bool(test(value))

        except:
            pass

    return False


def is_net_ip4(value):
    """
    Determine if this given value is an IPv4 network value or an IPv4 interface value;
    as defined by the ipaddress module

    Parameters
    ----------
    value : str
        The value to check

    Returns
    -------
    bool
        True if the value is any valid IPv4 thing
        False otherwise
    """
    for test in [lambda x: ipaddress.IPv4Network(x)._prefixlen != 32,
                 lambda x: ipaddress.IPv4Interface(x)._prefixlen != 32]:
        try:
            return bool(test(value))

        except:
            pass

    return False


def is_host_ip4(value):
    """
    Determine if this given value is an IPv4 address value as defined by the ipaddress module.

    Parameters
    ----------
    value : str
        The value to check

    Returns
    -------
    bool
        True if the value is any valid IPv4 thing
        False otherwise
    """
    try:
        return bool(ipaddress.IPv4Address(value))

    except:
        pass

    return False


# ----------------------------------------------------------------------------
# IPv6 functions
# ----------------------------------------------------------------------------

def is_any_ip6(value):
    """
    Determine if this given value is an IPv6 address, an IPv6 network value,
    or an IPv6 interface value as defined by the ipaddress module

    Parameters
    ----------
    value : str
        The value to check

    Returns
    -------
    bool
        True if the value is any valid IP thing
        False otherwise
    """
    for test in [ipaddress.IPv6Network, ipaddress.IPv6Interface, ipaddress.IPv6Address]:
        try:
            return bool(test(value))

        except:
            pass

    return False


def is_host_ip6(value):
    """
    Determine if this given value is an IPv6 address value as defined by the ipaddress module.

    Parameters
    ----------
    value : str
        The value to check

    Returns
    -------
    bool
        True if the value is any valid IP thing
        False otherwise
    """
    try:
        return bool(ipaddress.IPv6Address(value))

    except:
        pass


def is_net_ip6(value):
    """
    Determine if this given value is an IPv6 network value or an IPv6 interface value
    as defined by the ipaddress module

    Parameters
    ----------
    value : str
        The value to check

    Returns
    -------
    bool
        True if the value is any valid IP thing
        False otherwise
    """
    for test in [lambda x: ipaddress.IPv6Network(x)._prefixlen != 128,
                 lambda x: ipaddress.IPv6Interface(x)._prefixlen != 128]:
        try:
            return bool(test(value))

        except:
            pass

    return False


# -----------------------------------------------------------------------------------------------------------------
# IP any family
# -----------------------------------------------------------------------------------------------------------------

def is_any_ip(value):
    """
    Determine if this given value is an IP address, an IP network value, or an IP interface value;
    as defined by the ipaddress module; either IPv4 or IPv6.

    Parameters
    ----------
    value : str
        The value to check

    Returns
    -------
    bool
        True if the value is any valid IP thing
        False otherwise
    """
    return is_any_ip4(value) or is_any_ip6(value)


def is_host_ip(value):
    """
    Determine if this given value is an IP address as defined by the ipaddress module;
    either IPv4 or IPv6.

    Parameters
    ----------
    value : str
        The value to check

    Returns
    -------
    bool
        True if the value is any valid IP address
        False otherwise
    """

    return is_host_ip4(value) or is_host_ip6(value)


def is_net_ip(value):
    """
    Determine if this given value is an IP network value, or an IP interface value;
    as defined by the ipaddress module; either IPv4 or IPv6.

    Parameters
    ----------
    value : str
        The value to check

    Returns
    -------
    bool
        True if the value is any valid IP thing
        False otherwise
    """

    return is_net_ip4(value) or is_net_ip6(value)


def ip_only(value):
    """
    Returns only the IP address string of the value provided.  The value could be either an IP address,
    and IP network or and IP interface as defined by the ipaddress module.

    Parameters
    ----------
    value : str
        The value to use

    Returns
    -------
    str
        The IP address only value, if the value provided was valid

    None
        If the value provided is not an IP thing
    """
    for test in [lambda x: str(ipaddress.ip_address(x)),
                 lambda x: str(ipaddress.ip_interface(x).ip),
                 lambda x: str(ipaddress.ip_network(x).network_address)]:
        try:
            return test(value)

        except:
            pass

    return None


def in_subnet(value, subnet):
    """
    Determines if the given value (ip thing) is within the given IP subnet

    Parameters
    ----------
    value : str
        The IP thing to check

    subnet : str
        A valid IP subnet string

    Returns
    -------
    bool
        True if the value is in the subnet
        False otherwise; which could be the case if the value is not an IP thing.
    """
    return ipaddress.ip_address(ip_only(value)) in ipaddress.ip_network(subnet)


# -----------------------------------------------------------------------------------------------------------------
# These functions are bound into the LXML namespace.  See extension documentation for details
# https://lxml.de/1.3/extensions.html
# -----------------------------------------------------------------------------------------------------------------

def make_nsf(func):

    @wraps(func)
    def wrapper(dummy, ele):
        try:
            return func(ele[0].text)
        except:
            return False

    return wrapper


def nsf_in_subnet(dummy, ele, subnet):
    """
    lxml extension function wrapping in_subnet

    Parameters
    ----------
    dummy
        Not used

    ele : Element
        The lxml element to check

    subnet : str
        The subnet string value

    Returns
    -------
    bool
        True if the given element text value is an IP thing and is within the given subnet value
        False otherwise
    """
    try:
        value = ele[0].text
        return in_subnet(value, subnet)

    except:
        return False


# -----------------------------------------------------------------------------------------------------------------
# Bind functions into LXML namespace object
# -----------------------------------------------------------------------------------------------------------------

_ns_ext['is-any-ip'] = make_nsf(is_any_ip)
_ns_ext['is-host-ip'] = make_nsf(is_host_ip)
_ns_ext['is-net-ip'] = make_nsf(is_net_ip)

_ns_ext['is-any-ip6'] = make_nsf(is_any_ip6)
_ns_ext['is-net-ip6'] = make_nsf(is_net_ip6)
_ns_ext['is-host-ip6'] = make_nsf(is_host_ip6)

_ns_ext['is-any-ip4'] = make_nsf(is_any_ip4)
_ns_ext['is-net-ip4'] = make_nsf(is_net_ip4)
_ns_ext['is-host-ip4'] = make_nsf(is_host_ip4)

_ns_ext['in-subnet'] = nsf_in_subnet
