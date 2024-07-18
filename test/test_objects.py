from txtobj.objects import token, lines, TextObject
from txtobj.machinery.evaluator import evaluate_block_contents



def test_evaluate_in_block():
    obj = TextObject(
        bounds=("```", "````"),
        contents=[
            token(name="lang"),
            lines(name="body")
        ]
    )

    block = b"""
    python
    def hello():
        print("hello")
        print("hello again")
    """

    result = evaluate_block_contents(obj, block)
    assert result == {
        "lang": b"python",
        "body": [
            b"def hello():",
            b'print("hello")',
            b'print("hello again"'
        ]
    }