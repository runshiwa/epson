import xml.etree.ElementTree
import json
import sys

from . import common

ATTRIBUTE = "attribute"
TEXT = "text"
CHILDREN = "children"
TAIL = "tail"


def xml2dom(xml_string, *arg, **kwarg):
    return xml.etree.ElementTree.fromstring(xml_string, *arg, **kwarg)


def simplify_element(element):
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


def simplify_object(o):
    tag = next(iter(o))
    if isinstance(o[tag], dict):
        for key in o[tag].copy():
            if o[tag][key] is None or len(o[tag][key]) == 0:
                del o[tag][key]
        if len(o[tag]) == 1:
            o[tag] = o[tag][next(iter(o[tag]))]
        if len(o[tag]) == 0:
            o[tag] = None
    if isinstance(o[tag], list):
        candidate = []
        for index, item in enumerate(o[tag]):
            if item is None or len(item) == 0:
                candidate += [index]
        for index in reversed(candidate):
            del o[tag][index]
        if len(o[tag]) == 1:
            o[tag] = o[tag][0]
        if len(o[tag]) == 0:
            o[tag] = None
    if o[tag] is None:
        del o[tag]
    if len(o) == 1:
        o = o[next(iter(o))]
    if o is not None and len(o) == 0:
        o = None
    return o


def dom2object(element, strip=True, simplify=True, simplify2=False):
    # element is object with tag name
    o = {}
    # element has 0: attributes, 1: text, 2: child(ren), 3: tail as list
    o[element.tag] = {}

    # append element attributes
    o[element.tag][ATTRIBUTE] = {}
    for attrib in element.attrib:
        o[element.tag][ATTRIBUTE][attrib] = element.attrib[attrib]

    # append element text
    o[element.tag][TEXT] = element.text

    # append element child(ren)
    o[element.tag][CHILDREN] = []
    for child in element:
        o[element.tag][CHILDREN] += [
            dom2object(child, strip, simplify, simplify2)]

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
        o[element.tag] = simplify_element(o[element.tag])
    if simplify2:
        o = simplify_object(o)

    return o


def object2json(o, *arg, **kwarg):
    return json.dumps(o, *arg, **kwarg)


def process_content(dom, strip=True, simplify=True, simplify2=False, writer=print, writer_kwarg=None):
    if writer_kwarg is None:
        if writer == print:
            writer_kwarg = dict(end="")
        else:
            writer_kwarg = {}

    o = dom2object(dom, strip, simplify, simplify2)
    json_content = object2json(o, **common.JSON_DUMP_KWARG)
    writer(json_content, **writer_kwarg)


def process_file(xml_file, stdin="-"):
    if xml_file != stdin:
        with open(xml_file, newline="") as xf:
            dom = xml2dom(xf.read())
    else:
        dom = xml2dom(sys.stdin.read())
    process_content(dom)


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
