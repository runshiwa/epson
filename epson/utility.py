import random

from . import common

def random_string(charset=common.EPSON_STRING_GUARD_CS, length=common.EPSON_STRING_GUARD_LEN):
    return "".join(random.choices(charset, k=length))
