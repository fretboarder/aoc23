from pathlib import Path
from typing import Callable

Line = str


def get_input[T](
    inputfile: Path, line_parser: Callable[[Line], T] = lambda l: l
) -> list[T]:
    with inputfile.open("r") as f:
        return [line_parser(line) for line in f.read().split("\n")]
