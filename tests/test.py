from lxml import etree
import pylxmlextipaddress
import ipaddress

config = etree.parse(open('config.xml')).getroot()
ns = {'ip': pylxmlextipaddress.NAMESPACE}

print("""

ns = {'ip': pylxmlextipaddress.NAMESPACE}   # loaded

config.xpath('//*[ip:is-any-ip(.)]', namespaces=ns)
config.xpath('//*[ip:in-subnet(., "172.18.0.0/16")]', namespaces=ns)
""")
