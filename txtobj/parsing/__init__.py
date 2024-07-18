import os
import ctypes
import sysconfig
from pathlib import Path
from contextlib import contextmanager
from typing import List, Tuple, Generator

def __load_libarary():
    here = Path(__file__).parent.parent.absolute()
    suffix = sysconfig.get_config_var('EXT_SUFFIX')
    library_path = here.joinpath("parsing" + suffix)
    _c = ctypes.CDLL(str(library_path))
    return _c



class _Bounds(ctypes.Structure):
    _fields_ = [
        ("start", ctypes.c_long),
        ("end", ctypes.c_long),
    ]

class _BoundsList(ctypes.Structure):
    _fields_ = [
        ("bounds", ctypes.POINTER(_Bounds)),
        ("size", ctypes.c_int),
    ]


__c = __load_libarary()
__get_bounds = __c.get_bounds
__get_bounds.restype = _BoundsList
__get_bounds.argtypes = [
    ctypes.c_char_p, # file path
    ctypes.c_char_p, # start_token
    ctypes.c_int,  # len(start_token)
    ctypes.c_char_p, # end_token
    ctypes.c_int # len(end_token)
]

__free_bounds = __c.free_bounds
__free_bounds.restype = None
__free_bounds.argtypes = [_BoundsList]


@contextmanager
def blocks(
    path: os.PathLike,
    start_token: str,
    end_token: str,
) -> Generator[List[Tuple[int, int]], None, None]:
    bounds: _BoundsList = __get_bounds(
        str(path).encode("utf-8"),
        start_token.encode("utf-8"),
        len(start_token),
        end_token.encode("utf-8"),
        len(end_token),
    )
    try:
        yield [(b.start, b.end) for b in bounds.bounds[0:bounds.size]]
    finally:
        __free_bounds(bounds)