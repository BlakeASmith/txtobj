from pathlib import Path
from txtobj import parsing

TEST_PATH = Path(__file__).parent / "test.txt"


def test_get_block_bounds_finds_block():
    with parsing.get_block_bounds(TEST_PATH, "---\n", "\n---") as bounds:
        a, b = bounds[0]

        with open(TEST_PATH, "rb") as f:
            f.seek(a)
            v = f.read(b - a)

        assert v == b"foo: true\nbar: dingo"
        assert len(bounds) == 1


def blocks(path, bounds):
    with open(path, "rb") as f:
        for a, b in bounds:
            f.seek(a)
            yield f.read(b - a)


def test_get_block_bounds_finds_multple_blocks():
    with parsing.get_block_bounds(TEST_PATH, "```", "```") as bounds:
        assert len(bounds) == 3
        values = [
            entry
            for block in blocks(TEST_PATH, bounds)
            for entry in block.strip().split(b"\n")
        ]
        print(values)
        assert values == [
            b"sh",
            b"command arg1 arg2",
            b"python",
            b'print("hello world")',
            b"sh foobar",
        ]
