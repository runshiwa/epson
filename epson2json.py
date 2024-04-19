import json
import sys

from . import common

def process_content(epson_content, writer=print, writer_kwarg=None):
    if writer_kwarg is None:
        if writer == print:
            writer_kwarg = dict(end="")
        else:
            writer_kwarg = {}

    last = 0
    for match in common.EPSON_STRING.finditer(epson_content):
        writer(match.string[last:match.start()], **writer_kwarg)
        writer(json.dumps(match.string[match.start() + len(common.EPSON_STRING_START + match[1] + "\n"):match.end() - len("\n" + match[1] + "\n")], **common.JSON_DUMP_KWARG), **writer_kwarg)
        last = match.end()
    writer(epson_content[last:], **writer_kwarg)

def process_file(epson_file, stdin="-"):
    with open(epson_file, newline="") if epson_file != stdin else sys.stdin as ef:
        epson_content = ef.read()
        process_content(epson_content)

def main():
    if len(sys.argv) < 2:
        sys.argv += ["-"]
    for epson_file in sys.argv[1:]:
        process_file(epson_file)

if __name__ == "__main__":
    main()
