

from re import Pattern
from txtobj.objects import TextObject


def _match_one(pattern: Pattern, block: bytes):
    m = pattern.match(block)
    if m is None:
        return None, block

    groups = m.groups()
    if len(groups) == 2:
        value = groups[1]
    else:
        value = groups[0]

    _, end = m.span()
    return value, block[end:]


def evaluate_block_contents(t: TextObject, block: bytes):
    result = {}
    for placeholder in t.contents:
        name, pattern, n = placeholder

        if n == 1:
            value, block = _match_one(pattern, block)
            if value is None:
                return None
            if name:
                result[name] = value
        else:
            lst = []
            for _ in range(n):
                value, block = _match_one(pattern, block)
                if value is None:
                    break
                lst.append(value)
            if name:
                result[name] = lst

    print(result)
    return result