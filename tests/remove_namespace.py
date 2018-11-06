
from lxml.sax import ElementTreeContentHandler
from xml.sax.saxutils import XMLFilterBase


class RemoveNamespaces(XMLFilterBase):

    def __init__(self, parent=None):
        super(RemoveNamespaces, self).__init__(parent=parent)
        self._etree_handler = ElementTreeContentHandler()

    @property
    def etree(self):
        return self._etree_handler.etree

    def startElement(self, name, attrs):

        keep_attrs = {
            orig_name.rpartition(':')[-1]: attr_value
            for orig_name, attr_value in attrs.items()
            if not orig_name.startswith('xmlns')
        }

        self._etree_handler.startElement(name, keep_attrs)

    def endElement(self, name):
        self._etree_handler.endElement(name)

    def characters(self, content):
        self._etree_handler.characters(content.strip())




# demo:
# def from_file(filename):
#     reader = xml.sax.make_parser()
#     handler = RemoveNamespaces()
#     reader.setContentHandler(handler)
#     reader.parse(filename)
#     return handler.etree

from lxml import etree
from lxml.etree import XMLParser
import re
strip_ns = re.compile(b'xmlns=\"[^"]+\"|xmlns:\w+=\"[^"]+\"')


class ParseStripNS(XMLParser):
    def feed(self, data):
        newdata = strip_ns.sub(b'', data)
        super(ParseStripNS, self).feed(newdata)


class BuildTreeNoNS(etree.TreeBuilder):

    def start(self, tag, attrib, nsmap=None):
        no_ns_attrib = {
            orig_name.rpartition(':')[-1]: attr_value
            for orig_name, attr_value in attrib.items()
        }

        return super(BuildTreeNoNS, self).start(tag, no_ns_attrib, nsmap)

    def data(self, data):
        return super(BuildTreeNoNS, self).data(data.strip())


def make_parser():
    return ParseStripNS(target=BuildTreeNoNS())


def from_file(filename):
    parser = ParseStripNS(target=BuildTreeNoNS())
    parser.feed(open(filename, 'rb').read())
    return parser.close()

