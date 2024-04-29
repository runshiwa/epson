import random
import itertools


def random_string(charset, length):
    return "".join(random.choices(charset, k=length))


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


def remove_indent(multiline_string):
    valid_line = [
        line
        for line in multiline_string.splitlines()
        if line.strip()
    ]
    common_prefix = "".join(
        s[0]
        for s in itertools.takewhile(lambda x: all(x[0].isspace() and x[0] == c for c in x), zip(*valid_line))
    )
    multiline_string = "\n".join(
        line.removeprefix(common_prefix)
        for line in multiline_string.splitlines()
    )
    return multiline_string
