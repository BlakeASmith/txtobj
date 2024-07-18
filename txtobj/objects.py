import re
from dataclasses import dataclass
import sys
from typing import List, Tuple

type Bounds = Tuple[str, str]
type Placeholder = Tuple[str | None, re.Pattern, int]


_REPEAT_UNTIL_END_OF_BLOCK = sys.maxsize

def token(name: str | None = None) -> Placeholder:
    return (name, re.compile(b"\\s*(\\w+)\\s*"), 1)


def lines(name: str, n: int=_REPEAT_UNTIL_END_OF_BLOCK) -> Placeholder:
    return (name, re.compile(b"\\s*(.+)\\s*"), n)


@dataclass
class TextObject:
    bounds: Tuple
    contents: List[Placeholder]

