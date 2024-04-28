import xml.etree.ElementTree
import xml.dom.minidom
import json
import sys

from . import common

ATTRIBUTE = "attribute"
TEXT = "text"
CHILDREN = "children"
TAIL = "tail"   # ElementTree only


def xml2etdom(xml_string, *arg, **kwarg):
    return xml.etree.ElementTree.fromstring(xml_string, *arg, **kwarg)


def xml2dom(xml_string, *arg, **kwarg):
    return xml.dom.minidom.parseString(xml_string, *arg, **kwarg)


def simplify_etelement(element):
    if len(element[ATTRIBUTE]) == 0:
        del element[ATTRIBUTE]
    if len(element[CHILDREN]):
        del element[TEXT]
        del element[TAIL]
    else:
        if element[TEXT] is None:
            del element[TEXT]
        del element[CHILDREN]
        del element[TAIL]
    return element


def simplify_element(element):
    if len(element[ATTRIBUTE]) == 0:
        del element[ATTRIBUTE]
    if len(element[CHILDREN]):
        del element[TEXT]
    else:
        if element[TEXT] is None:
            del element[TEXT]
        del element[CHILDREN]
    return element


def simplify_object(obj):
    if isinstance(obj, dict):
        obj = {
            key: item
            for key, item in obj.items()
            if item
        }
        if len(obj) == 1:
            return obj.popitem()[1]
        elif len(obj) == 0:
            return None
    elif isinstance(obj, list):
        obj = [
            item
            for item in obj
            if item
        ]
        if len(obj) == 1:
            return obj[0]
        elif len(obj) == 0:
            return None
    return obj


def etdom2object(element, strip=True, simplify=True, simplify2=False):
    # element is object with tag name
    o = {}
    # element has attributes, text, child(ren), tail as list
    o[element.tag] = {}

    # append element attributes
    o[element.tag][ATTRIBUTE] = {}
    for attribute in element.attrib:
        o[element.tag][ATTRIBUTE][attribute] = element.attrib[attribute]

    # append element text
    o[element.tag][TEXT] = element.text

    # append element child(ren)
    o[element.tag][CHILDREN] = []
    for child in element:
        o[element.tag][CHILDREN] += [
            etdom2object(child, strip, simplify, simplify2)]

    # append element tail
    o[element.tag][TAIL] = element.tail

    if strip:
        if o[element.tag][TEXT] is not None:
            o[element.tag][TEXT] = o[element.tag][TEXT].strip()
            if len(o[element.tag][TEXT]) == 0:
                o[element.tag][TEXT] = None
        if o[element.tag][TAIL] is not None:
            o[element.tag][TAIL] = o[element.tag][TAIL].strip()
            if len(o[element.tag][TAIL]) == 0:
                o[element.tag][TAIL] = None
    if simplify:
        o[element.tag] = simplify_etelement(o[element.tag])
    if simplify2:
        o[element.tag] = simplify_object(o[element.tag])

    return o


def dom2object(element, strip=True, simplify=True, simplify2=False):
    # element is object with tag name
    o = {}
    # element has attributes, text, child(ren)
    o[element.tagName] = {}

    # append element attributes
    o[element.tagName][ATTRIBUTE] = {}
    for attribute in element.attributes if element.attributes else {}:
        o[element.tagName][ATTRIBUTE][attribute.name] = attribute.value

    # append element text
    o[element.tagName][TEXT] = "".join(
        child.data for child in element.childNodes if child.nodeType == xml.dom.Node.TEXT_NODE)

    # append element child(ren)
    o[element.tagName][CHILDREN] = []
    for child in element.childNodes:
        if child.nodeType == xml.dom.Node.ELEMENT_NODE:
            o[element.tagName][CHILDREN] += [
                dom2object(child, strip, simplify, simplify2)]

    if strip:
        if o[element.tagName][TEXT] is not None:
            o[element.tagName][TEXT] = o[element.tagName][TEXT].strip()
            if len(o[element.tagName][TEXT]) == 0:
                o[element.tagName][TEXT] = None
    if simplify:
        o[element.tagName] = simplify_element(o[element.tagName])
    if simplify2:
        o[element.tagName] = simplify_object(o[element.tagName])

    return o


def object2json(o, *arg, **kwarg):
    return json.dumps(o, *arg, **kwarg)


def process_content(xml_content, strip=True, simplify=True, simplify2=True, writer=print, writer_kwarg=None):
    if writer_kwarg is None:
        if writer == print:
            writer_kwarg = dict(end="")
        else:
            writer_kwarg = {}

    if False:
        dom = xml2etdom(xml_content)
        o = etdom2object(dom, strip, simplify, simplify2)
    else:
        dom = xml2dom(xml_content)
        o = dom2object(dom.documentElement, strip, simplify, simplify2)
    json_content = object2json(o, **common.JSON_DUMP_KWARG)
    writer(json_content, **writer_kwarg)


def process_file(xml_file, stdin="-"):
    if xml_file != stdin:
        with open(xml_file, newline="") as xf:
            xml_content = xf.read()
    else:
        xml_content = sys.stdin.read()
    process_content(xml_content)


def main():
    if len(sys.argv) < 2:
        sys.argv += ["-"]
    for xml_file in sys.argv[1:]:
        process_file(xml_file)


if __name__ == "__main__":
    import io
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, newline="")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, newline="")

    main()
