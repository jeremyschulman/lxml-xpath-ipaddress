
from lxml import etree
from lxml.etree import XMLParser
import re

# the following regular expression is used to find the XML namespace assignment values
# in elements. the form can be either the default namespace (xmlns) or a namespace
# assignment, for example xmlns:junos="...".

XML_ELEMENT_NS_REGEXP = 'xmlns=\"[^"]+\"|xmlns:\w+=\"[^"]+\"'


class ParseBytesStripNS(XMLParser):
    """
    XMLParser subclass used to remove XML namespaces when the content provided is bytes.
    """
    strip_ns = re.compile(XML_ELEMENT_NS_REGEXP.encode('u8'))

    def feed(self, data):
        newdata = ParseBytesStripNS.strip_ns.sub(b'', data)
        super(ParseBytesStripNS, self).feed(newdata)


class ParseStripNS(XMLParser):
    """
    XMLParser subclass used to remove XML namespaces when the content provided is str.
    """
    strip_ns = re.compile(XML_ELEMENT_NS_REGEXP)

    def feed(self, data):
        newdata = ParseStripNS.strip_ns.sub('', data)
        super(ParseStripNS, self).feed(newdata)


class BuildTreeNoNS(etree.TreeBuilder):
    """
    BuildTreeNoNS is an LXML SAX parser target class that will construct an LXML
    ElementTree.  This class is used to perform two transformation on the XML data as it
    is being SAX processed and built into an ElementTree:

        1) remove namespaces from element attributes

        2) remove CRLF from the data; i.e. "normalize=True"

    This class is meant to be used in combination with the above ParseStripNS or
    ParserBytesStripNS parser classes; which are used to remove namespace values from
    the element tags as they are being feed into the SAX processor.
    """

    def start(self, tag, attrib, nsmap=None):
        """
        SAX event handler the 'start tag' event.  This method strips any namespace values
        from the attributes.

        Parameters
        ----------
        tag : str
            The element tag value

        attrib : dict
            The element attribute dictionary

        nsmap : dict
            The element namepsace-map dictionary

        Returns
        -------
        The value from TreeBuilder.start() providing the attributes without namespaces.
        """

        # iterate through the attributes and use only the non-namespace attribute
        # name.  The rpartition use handles the case when the attribute does not
        # have a namespace as well.

        no_ns_attrib = {
            orig_name.rpartition(':')[-1]: attr_value
            for orig_name, attr_value in attrib.items()
        }

        return super(BuildTreeNoNS, self).start(tag, no_ns_attrib, nsmap)

    def data(self, data):
        """
        SAX event handler for any data value.  This method strips the CRLR from the data
        in the same manner as "normalize=True" is used.

        Parameters
        ----------
        data : str
            The original data

        Returns
        -------
        The value from TreeBuilder.data() providing the stripped data.
        """
        return super(BuildTreeNoNS, self).data(data.strip())


def from_file(filename, mode='r', size=2048):
    """
    This funciton will read XML from `filename` and return an LXML ElementTree.  The
    contents of `filename` are read in chunks of `size` and feed into an LXML SAX processor
    so that the namespaces are removed, and data is stripped of CRLF; using the parser classes
    and parser targets provided by this module.

    Parameters
    ----------
    filename : str
        Path to XML file

    mode : str
        The mode to open the file.  This is 'r' by default, but if you are reading in a byte file
        then you should use 'rb'

    size : int
        The size of the chunks to read from the file.

    Returns
    -------
    ElementTree:
        The resulting LXML ElementTree object resulting from the SAX processing.
    """

    parser = ParseBytesStripNS if 'b' in mode else ParseStripNS
    reader = parser(target=BuildTreeNoNS())
    ifile = open(filename, mode)

    while True:
        data = ifile.read(size)
        if not data:
            break
        reader.feed(data)

    return reader.close()

