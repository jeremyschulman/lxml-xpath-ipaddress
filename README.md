# LXML Extension Library for IP address

This library contains LXML extension functions that wrap the Python ipaddress library.

With this library in place, you can do XPath expressions to find IP items within our XML data.  For
example:

````python
from lxml import etree
from lxml_xpath_ipaddress import ip_ns

# given "config" is an LXML XML structure, you can run the XPath to find all IPv4 network items:

config = etree.parse('tests/config.xml')


items = config.xpath('//*[ip:ip4-net(.)', namespaces=ip_ns)

print(items[0].text)
# >>> 10.10.0.0/16

# Find all items that are in either the 172.18/16 or 101.10.201/24 subnets

items = config.xpath('//*[ip:in-subnet(., "172.18.0.0/16") or ip:in-subnet(., "10.10.201.0/24")]',
                     namespaces=ip_ns)
                     
print(items[0].text)
# >>> 172.18.1.1
````

# Install

```bash
$ pip install lxml-xpath-ipaddress
```

# LXML Extension Functions

## Either IPv4 or IPv6

  * ip-any(value)
  * ip-net(value)
  * ip-host(value)
  
## IPv4

  * ip4-any(value)
  * ip4-net(value)
  * ip4-host(value)

## IPv6
  
  * ip6-any(value)
  * ip6-net(value)
  * ip6-host(value)

## Subnet Checking

  * in-subnet(value, subnet-string)
  
# Python Functions

The library contains these functions as general purpose functions as well, 
so that they can be used in other applications.  See the module doc-strings for use.  

  