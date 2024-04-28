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
            obj = obj.popitem()[1]
        elif len(obj) == 0:
            obj = None
    elif isinstance(obj, list):
        obj = [
            item
            for item in obj
            if item
        ]
        if len(obj) == 1:
            obj = obj[0]
        elif len(obj) == 0:
            obj = None
    return obj


def etdom2object(element, strip=True, simplify=True, simplify2=False):
    # element is object with tag name
    element_object = {}
    # element has attributes, text, child(ren), tail as list
    element_object[element.tag] = {}

    # append element attributes
    element_object[element.tag][ATTRIBUTE] = {}
    for attribute in element.attrib:
        element_object[element.tag][ATTRIBUTE][attribute] = element.attrib[attribute]

    # append element text
    element_object[element.tag][TEXT] = element.text

    # append element child(ren)
    element_object[element.tag][CHILDREN] = []
    for child in element:
        element_object[element.tag][CHILDREN] += [
            etdom2object(child, strip, simplify, simplify2)]

    # append element tail
    element_object[element.tag][TAIL] = element.tail

    if strip:
        if element_object[element.tag][TEXT] is not None:
            element_object[element.tag][TEXT] = element_object[element.tag][TEXT].strip()
            if len(element_object[element.tag][TEXT]) == 0:
                element_object[element.tag][TEXT] = None
        if element_object[element.tag][TAIL] is not None:
            element_object[element.tag][TAIL] = element_object[element.tag][TAIL].strip()
            if len(element_object[element.tag][TAIL]) == 0:
                element_object[element.tag][TAIL] = None
    if simplify:
        element_object[element.tag] = simplify_etelement(element_object[element.tag])
    if simplify2:
        element_object[element.tag] = simplify_object(element_object[element.tag])

    return element_object


def dom2object(element, strip=True, simplify=True, simplify2=False):
    # element is object with tag name
    element_object = {}
    # element has attributes, text, child(ren)
    element_object[element.tagName] = {}

    # append element attributes
    element_object[element.tagName][ATTRIBUTE] = {}
    for attribute, value in element.attributes.items():
        element_object[element.tagName][ATTRIBUTE][attribute] = value

    # append element text
    element_object[element.tagName][TEXT] = "".join(
        child.data for child in element.childNodes if child.nodeType == xml.dom.Node.TEXT_NODE)

    # append element child(ren)
    element_object[element.tagName][CHILDREN] = []
    for child in element.childNodes:
        if child.nodeType == xml.dom.Node.ELEMENT_NODE:
            element_object[element.tagName][CHILDREN] += [
                dom2object(child, strip, simplify, simplify2)]

    if strip:
        if element_object[element.tagName][TEXT] is not None:
            element_object[element.tagName][TEXT] = element_object[element.tagName][TEXT].strip()
            if len(element_object[element.tagName][TEXT]) == 0:
                element_object[element.tagName][TEXT] = None
    if simplify:
        element_object[element.tagName] = simplify_element(element_object[element.tagName])
    if simplify2:
        element_object[element.tagName] = simplify_object(element_object[element.tagName])

    return element_object


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
