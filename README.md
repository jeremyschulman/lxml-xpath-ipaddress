# LXML Extension Library for IP address

This library contains LXML extension functions that wrap the Python ipaddress library.

With this library in place, you can do XPath expressions to find IP items within our XML data.  For
example:

````python
from lxml import etree
import pylxmlextipaddress

# given "config" is an LXML XML structure, you can run the XPath to find all IPv4 network items:

config = etree.parse('tests/config.xml').getroot()

ns = {'ip': pylxmlextipaddress.NAMESPACE}

items = config.xpath('//*[ip:is-net-ip4(.)', namespaces=ns)

print(items[0].text)
# >>> 10.10.0.0/16

# Find all items that are in either the 172.18/16 or 101.10.201/24 subnets

items = config.xpath('//*[ip:in-subnet(., "172.18.0.0/16") or ip:in-subnet(., "10.10.201.0/24")]', namespaces=ns)
print(items[0].text)
# >>> 172.18.1.1
````


# Install

```bash
$ python setup.py install
```

Will be posted to PyPI soon ... 

# LXML Extension Functions

## Either IPv4 or IPv6

  * is-any-ip(value)
  * is-net-ip(value)
  * is-host-ip(value)
  
## IPv4

  * is-any-ip4(value)
  * is-net-ip4(value)
  * is-host-ip4(value)

## IPv6
  
  * is-any-ip6(value)
  * is-net-ip6(value)
  * is-host-ip6(value)

## Subnet Checking

  * in-subnet(value, subnet-string)
  
# Python Functions

The library contains these functions as general purpose functions as well, so that they can be used in other
applications.  See the module doc-strings for use.  
  