
from lxml.sax import ElementTreeContentHandler
from xml.sax.saxutils import XMLFilterBase
from xml.sax import make_parser


class RemoveNamespaces(XMLFilterBase):
    """
    This class implements the xml.sax.ContentHandler methods so that it can
    be used with XMLReader parser.  The function of this class is to build
    an LXML ElementTree using the lxml.sax.ElementTreeContentHandler.  THe
    methods in this class are used to intercept the SAX events so that:

        1) namespace values are removed - default namespaces and attribute namespaces
        2) CRLF are stripped from the element text

    This class can then be used as a base-class for more advanced XML SAX processing.
    """
    def __init__(self, parent=None):
        super(RemoveNamespaces, self).__init__(parent=parent)
        self._etree_handler = ElementTreeContentHandler()

    @property
    def etree(self):
        return self._etree_handler.etree

    def startElement(self, name, attrs):
        """
        This method is used to intercept the start element SAX events and remove
        the namespace values out of the attrs.  The namespace definitions are also
        located in the attrs, so we want to both discard these as well as remove the namespace
        prefix from the attributes we want to keep.  Once updated, this
        method then invokes the LXML ElementTree content handler start element so that
        the tree can be built.

        Parameters
        ----------
        name : str
            The element tag name.

        attrs : xml.sax.xmlreader.AttributesImpl
            The collections of element attributes
        """
        keep_attrs = {
            orig_name.rpartition(':')[-1]: attr_value
            for orig_name, attr_value in attrs.items()
            if not orig_name.startswith('xmlns')
        }

        self._etree_handler.startElement(name, keep_attrs)

    def endElement(self, name):
        """
        This method is used to intercept the SAX "end element" event and invoke the
        ElementTree handler.

        Parameters
        ----------
        name : str
            The element tag name
        """
        self._etree_handler.endElement(name)

    def characters(self, content):
        """
        This method is used to intercept the SAX "characters" event and invoke
        the Element tree handler with the content stripped for CRLR
        """
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
