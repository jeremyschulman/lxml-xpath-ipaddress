from lxml import etree


def ppxml(xml):
    print(etree.tostring(xml, encoding='unicode', pretty_print=True))


def indent(elem, level=0):

    spaces = f'\n{level * "  "}'

    if len(elem):

        if not elem.text:
            elem.text = f'{spaces}  '

        if not elem.tail:
            elem.tail = spaces

        for elem in elem:
            indent(elem, level + 1)

        if not elem.tail:
            elem.tail = spaces

    else:
        if level and not elem.tail:
            elem.tail = spaces
