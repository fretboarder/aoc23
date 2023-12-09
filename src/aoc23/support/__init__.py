import hashlib
from pathlib import Path
from typing import Protocol, TypeVar

T_co = TypeVar("T_co", covariant=True)


class LineParser(Protocol[T_co]):
    def __call__(self, line: str) -> T_co:
        ...


def default_parser(line: str) -> str:
    return line


def get_input(
    inputfile: Path,
    line_parser: LineParser[T_co] = default_parser,  # type: ignore  # noqa: PGH003
) -> list[T_co]:
    with inputfile.open("r") as f:
        return [line_parser(line) for line in f.read().split("\n")]


def sha256(input_string: str) -> str:
    # Convert the input string to bytes
    if isinstance(input_string, float | int):
        input_string = str(input_string)
    input_bytes = input_string.encode("utf-8")
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()
    # Update the hash object with the input bytes
    sha256_hash.update(input_bytes)
    # Get the hexadecimal digest
    return sha256_hash.hexdigest()
