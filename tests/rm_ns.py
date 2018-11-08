
from lxml.sax import ElementTreeContentHandler
from xml.sax.saxutils import XMLFilterBase
from xml.sax import make_parser


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


def from_file(filename, mode='r', size=4096):
    """
    This funciton will read XML from `filename` and return an LXML ElementTree.  The
    contents of `filename` are read in chunks of `size` and feed into an  SAX processor
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

    ifile = open(filename, mode)

    reader = make_parser()
    handler = RemoveNamespaces()
    reader.setContentHandler(handler)

    while True:
        data = ifile.read(size)
        if not data:
            break
        reader.feed(data)

    reader.close()
    return handler.etree
