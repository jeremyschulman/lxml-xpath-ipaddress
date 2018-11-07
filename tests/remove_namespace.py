
from lxml import etree
from lxml.etree import XMLParser
import re


class ParseBytesStripNS(XMLParser):
    """ if parsing byte content """
    strip_ns = re.compile(b'xmlns=\"[^"]+\"|xmlns:\w+=\"[^"]+\"')

    def feed(self, data):
        newdata = ParseBytesStripNS.strip_ns.sub(b'', data)
        super(ParseBytesStripNS, self).feed(newdata)


class ParseStripNS(XMLParser):
    """ if parsing str content """
    strip_ns = re.compile('xmlns=\"[^"]+\"|xmlns:\w+=\"[^"]+\"')

    def feed(self, data):
        newdata = ParseStripNS.strip_ns.sub('', data)
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


def from_file_chunked(filename, mode, size):

    parser = ParseBytesStripNS if 'b' in mode else ParseStripNS
    reader = parser(target=BuildTreeNoNS())
    ifile = open(filename, mode)

    while True:
        data = ifile.read(size)
        if not data:
            break
        reader.feed(data)

    return reader.close()

