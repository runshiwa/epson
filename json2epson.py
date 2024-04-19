import json
import sys

from . import common
from . import utility

def process_content(json_content, writer=print, writer_kwarg=None):
    if writer_kwarg is None:
        if writer == print:
            writer_kwarg = dict(end="")
        else:
            writer_kwarg = {}

    last = 0
    for match in common.JSON_STRING.finditer(json_content):
        json_string = match.string[match.start():match.end()]
        python_string = json.loads(json_string)
        line = python_string.split("\n")
        if 1 < len(line):
            guard = common.EPSON_STRING_GUARD
            while guard in line:
                guard = utility.random_string()
            writer(match.string[last:match.start()], **writer_kwarg)
            writer("\n".join([common.EPSON_STRING_START + guard, python_string, guard, ""]), **writer_kwarg)
        else:
            writer(match.string[last:match.end()], **writer_kwarg)
        last = match.end()
    writer(json_content[last:], **writer_kwarg)

def process_file(json_file, stdin="-"):
    with open(json_file, newline="") if json_file != stdin else sys.stdin as jf:
        json_content = jf.read()
        process_content(json_content)

def main():
    if len(sys.argv) < 2:
        sys.argv += ["-"]
    for json_file in sys.argv[1:]:
        process_file(json_file)

if __name__ == "__main__":
    main()
