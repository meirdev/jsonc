from pathlib import Path

import jsonc

BASE_DIR = Path(__file__).resolve().parent


def test_escape_string():
    file = r"""
{
    "a": "b\"",
    "c": "d\\e\\\n\\\\f"
}
    """

    assert jsonc.loads(file) == {"a": "b\"", "c": "d\\e\\\n\\\\f"}


def test_single_line_comment():
    file = """
{
    "a": "b",
    "c": "d"
    // "e": "f",
}
    """

    assert jsonc.loads(file) == {"a": "b", "c": "d"}


def test_single_line_comment_in_end_of_line():
    file = """
{
    "a": "b",
    "c": "d" // Here is a comment
}
    """

    assert jsonc.loads(file) == {"a": "b", "c": "d"}


def test_single_line_comment_in_eof():
    file = """
{
    "a": "b",
    "c": "d"
}// Here is a comment"""

    assert jsonc.loads(file) == {"a": "b", "c": "d"}


def test_multi_line_comment():
    file = """
{
    "a": "b"
    /*
    "c": "d",
    "e": "f"
    */
}
    """

    assert jsonc.loads(file) == {"a": "b"}


def test_single_line_comment_in_string():
    file = """
{
    "a": "b",
    "c": "d // This is not a comment"
}
    """

    assert jsonc.loads(file) == {"a": "b", "c": "d // This is not a comment"}


def test_multi_line_comment_in_string():
    file = """
{
    "a": "b",
    "c": "d /* This is not a comment */"
}
    """

    assert jsonc.loads(file) == {"a": "b", "c": "d /* This is not a comment */"}


def test_trailing_comma():
    file = """
{
    "a": "b",
    "c": "d",
}
    """

    assert jsonc.loads(file, allow_trailing_comma=True) == {"a": "b", "c": "d"}


def test_trailing_comma_in_array():
    file = """
{
    "a": ["b", "c",]
}
    """

    assert jsonc.loads(file, allow_trailing_comma=True) == {"a": ["b", "c"]}


def test_complex():
    file = """
{
    "a": "b",
    "c": "d", // Here is a comment
    /*
    "e": "f",
    "g": "h"
    */
    "// not a comment": "i",
    "j": "k /* not a comment */",
}
    """

    assert jsonc.loads(file, allow_trailing_comma=True) == {
        "a": "b",
        "c": "d",
        "// not a comment": "i",
        "j": "k /* not a comment */",
    }


def test_from_file():
    with open(BASE_DIR / "test_file.jsonc") as fp:
        assert jsonc.load(fp, allow_trailing_comma=True) == {
            "why": "leaving",
            "clearly": -951479207.845695,
            "realize": [
                87359115,
                "teacher",
                [
                    True,
                    False,
                    False,
                    -708970086,
                    False,
                    1176095491,
                ],
                True,
                "troops",
                "college",
            ],
            "clothes": "scale",
            "cost": "ruler",
            "perfect": True,
        }
