import ctypes
import sysconfig
from pathlib import Path

def __load_libarary():
    here = Path(__file__).parent.parent.absolute()
    suffix = sysconfig.get_config_var('EXT_SUFFIX')
    library_path = here.joinpath("parsing" + suffix)
    _c = ctypes.CDLL(str(library_path))
    return _c


__c = __load_libarary()
__hello = __c.hello
__hello.restype = ctypes.c_char_p


def hello() -> str:
    return __c.hello()
