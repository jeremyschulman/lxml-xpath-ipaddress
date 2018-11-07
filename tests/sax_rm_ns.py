#
# from lxml.sax import ElementTreeContentHandler
# from xml.sax.saxutils import XMLFilterBase
#
#
# class RemoveNamespaces(XMLFilterBase):
#
#     def __init__(self, parent=None):
#         super(RemoveNamespaces, self).__init__(parent=parent)
#         self._etree_handler = ElementTreeContentHandler()
#
#     @property
#     def etree(self):
#         return self._etree_handler.etree
#
#     def startElement(self, name, attrs):
#
#         keep_attrs = {
#             orig_name.rpartition(':')[-1]: attr_value
#             for orig_name, attr_value in attrs.items()
#             if not orig_name.startswith('xmlns')
#         }
#
#         self._etree_handler.startElement(name, keep_attrs)
#
#     def endElement(self, name):
#         self._etree_handler.endElement(name)
#
#     def characters(self, content):
#         self._etree_handler.characters(content.strip())
#
#


# demo:
# def from_file(filename):
#     reader = xml.sax.make_parser()
#     handler = RemoveNamespaces()
#     reader.setContentHandler(handler)
#     reader.parse(filename)
#     return handler.etree
