import json
import sys

from . import common
from . import utility

def process_content(json_content, writer=print, writer_kwarg=None, line_threshold=common.JSON_STRING_LINE_THRESHOLD, guard_default=common.EPSON_STRING_GUARD):
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
        if line_threshold < len(line):
            guard = guard_default
            while guard in line:
                guard = utility.random_string(charset=common.EPSON_STRING_GUARD_CS, length=common.EPSON_STRING_GUARD_LEN)
            writer(match.string[last:match.start()], **writer_kwarg)
            writer("\n".join([common.EPSON_STRING_START + guard, python_string, guard, ""]), **writer_kwarg)
        else:
            writer(match.string[last:match.end()], **writer_kwarg)
        last = match.end()
    writer(json_content[last:], **writer_kwarg)

def process_file(json_file, stdin="-", line_threshold=common.JSON_STRING_LINE_THRESHOLD):
    with open(json_file, newline="") if json_file != stdin else sys.stdin as jf:
        json_content = jf.read()
        process_content(json_content, line_threshold=line_threshold)

def main():
    if len(sys.argv) < 2:
        sys.argv += ["-"]
    for json_file in sys.argv[1:]:
        process_file(json_file)

if __name__ == "__main__":
    import io
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, newline="")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, newline="")

    main()
