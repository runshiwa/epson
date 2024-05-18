import re
import string

EPSON_STRING = re.compile(r'""([^,]+)\n(.*\n)*?\1\n')
EPSON_STRING_START = '""'
EPSON_STRING_GUARD = "."
EPSON_STRING_GUARD_CS = string.ascii_letters + string.digits
EPSON_STRING_GUARD_LEN = 9

JSON_STRING = re.compile(r'"((?:\\.|[^"\\])*)"')
JSON_STRING_LINE_THRESHOLD = 1
JSON_DUMP_KWARG = dict(ensure_ascii=False, indent="\t", default=repr)
