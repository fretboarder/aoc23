import re
from dataclasses import dataclass
from pathlib import Path
from pprint import pp

from aoc23.support import get_input


@dataclass(frozen=True)
class ValueCoord:
    value: int
    row: int
    col_begin: int
    col_end: int


@dataclass(frozen=True)
class Pos:
    col: int
    row: int


def parse_input(lines: list[str]) -> tuple[list[Pos], set[ValueCoord]]:
    symbols: list[Pos] = []
    coords: set[ValueCoord] = set()
    for irow, row in enumerate(lines):
        for icol, col in enumerate(row):
            if not col.isdigit() and col != ".":
                symbols.append(Pos(icol, irow))
        coords |= parse_numbers(row, irow)
    return symbols, coords


def parse_numbers(line: str, row: int) -> set[ValueCoord]:
    matches = re.finditer(r"\d+", line)
    return {
        ValueCoord(int(match.group()), row, match.start(), match.end() - 1)
        for match in matches
    }


def get_adjacent(sym: Pos, value_coords: set[ValueCoord]) -> set[ValueCoord]:
    matches: set[ValueCoord] = set()
    for vco in value_coords:
        # is there a number next to the symbol in the same or surrounding rows?
        if (
            vco.row in (sym.row - 1, sym.row, sym.row + 1)
            and vco.col_begin - 1 <= sym.col <= vco.col_end + 1
        ):
            matches.add(vco)

    return matches


def collect_adjacent(symbols: list[Pos], value_coords: set[ValueCoord]) -> int:
    coords: set[ValueCoord] = set()
    for sym in symbols:
        if c := get_adjacent(sym, value_coords):
            coords |= c
    return sum(c.value for c in coords)


def collect_adjacent2(symbols: list[Pos], value_coords: set[ValueCoord]) -> int:
    gear: list[int] = []
    for sym in symbols:
        if (c := get_adjacent(sym, value_coords)) and len(c) == 2:  # noqa: PLR2004
            a, b = (co.value for co in c)
            gear.append(a * b)
    return sum(gear)


def main() -> tuple[int, int]:
    # Build a list of Values and their coordinates
    lines1: list[str] = get_input(Path(__file__).parent / "input01.txt")
    symbols, value_coords = parse_input(lines1)
    value = collect_adjacent(symbols, value_coords)
    gear = collect_adjacent2(symbols, value_coords)
    return value, gear


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")
