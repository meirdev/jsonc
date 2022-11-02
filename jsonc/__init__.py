import json
import string
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from _typeshed import SupportsRead

RangeResult = tuple[int, int]

JSON = Any


def _is_escaped(file: str, index: int) -> bool:
    start = index - 1
    while file[start] == "\\":
        start -= 1
    return (index - start + 1) % 2 != 0


def _is_eof(file: str, index: int) -> bool:
    return len(file) == index


def _is_whitespace(file: str, index: int) -> RangeResult | None:
    end = index
    while file[end] in string.whitespace:
        end += 1
    if end != index:
        return index, end
    return None


def _is_string(file: str, index: int) -> RangeResult | None:
    if file[index] == '"':
        end = index + 1
        while not (file[end] == '"' and not _is_escaped(file, end)):
            end += 1
        return index, end + 1
    return None


def _is_single_line_comment(file: str, index: int) -> RangeResult | None:
    if file[index] == "/" and file[index + 1] == "/":
        end = index + 2
        while not _is_eof(file, end) and file[end] != "\n":
            end += 1
        return index, end + 1
    return None


def _is_multi_line_comment(file: str, index: int) -> RangeResult | None:
    if file[index] == "/" and file[index + 1] == "*":
        end = index + 2
        while file[end] != "*" or file[end + 1] != "/":
            end += 1
        return index, end + 2
    return None


def _is_trailing_comma(file: str, index: int) -> RangeResult | None:
    if file[index] == ",":
        end = index + 1
        while (
            result := _is_whitespace(file, end)
            or _is_single_line_comment(file, end)
            or _is_multi_line_comment(file, end)
        ):
            end = result[1]
        if file[end] == "]" or file[end] == "}":
            return index, end
    return None


def loads(file: str, allow_trailing_comma: bool = False) -> JSON:
    new_file = []

    i = 0
    while i < len(file):
        if result := _is_string(file, i):
            new_file.append(file[i : result[1]])
            i = result[1]
            continue
        elif (
            (result := _is_single_line_comment(file, i))
            or (result := _is_multi_line_comment(file, i))
            or (allow_trailing_comma and (result := _is_trailing_comma(file, i)))
        ):
            i = result[1]
            continue

        new_file.append(file[i])
        i += 1

    return json.loads("".join(new_file))


def load(file: "SupportsRead[str]", allow_trailing_comma: bool = False) -> JSON:
    return loads(file.read(), allow_trailing_comma)
