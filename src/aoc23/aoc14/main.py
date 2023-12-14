from collections import Counter, defaultdict
from functools import cache
from pathlib import Path
from pprint import pp
from typing import NamedTuple

from aoc23.support import get_input


def parse_input(input_lines: list[str]) -> tuple[str, ...]:
    # create a frame around the grid, makes it easier
    new_input = ["#" * (len(input_lines[0]) + 2)]
    new_input += [f"#{l}#" for l in input_lines]
    new_input += ["#" * (len(input_lines[0]) + 2)]
    return tuple(new_input)


@cache
def find_indexes(input_string: str, char: str):
    return [index for index, value in enumerate(input_string) if value == char]


@cache
def rearrange(input_string: str) -> str:
    c = Counter(input_string)
    return "O" * c["O"] + "." * c["."]


@cache
def tilt(input_string: str) -> str:
    blocks = find_indexes(input_string, "#")
    if not blocks:
        return input_string
    rearranged = ""
    p0 = blocks[0]
    for p1 in blocks[1:]:
        rearranged += "#" + rearrange(input_string[p0 + 1 : p1])
        p0 = p1
    return rearranged + "#"


@cache
def cols_to_rows(cols: tuple[str, ...]) -> tuple[str, ...]:
    split_columns = [list(x) for x in cols]
    return tuple(["".join(r) for r in list(zip(*split_columns))])


@cache
def tiltnorth(grid: tuple[str, ...]) -> tuple[str, ...]:
    new_grid = tuple([tilt(col) for col in cols_to_rows(grid)])
    return cols_to_rows(new_grid)


@cache
def tiltwest(grid: tuple[str, ...]) -> tuple[str, ...]:
    return tuple([tilt(col) for col in grid])


@cache
def tiltsouth(grid: tuple[str, ...]) -> tuple[str, ...]:
    new_grid = tuple([tilt(col[::-1])[::-1] for col in cols_to_rows(grid)])
    return cols_to_rows(new_grid)


@cache
def tilteast(grid: tuple[str, ...]) -> tuple[str, ...]:
    return tuple([tilt(col[::-1])[::-1] for col in grid])


@cache
def tiltcycle(grid: tuple[str, ...]) -> tuple[str, ...]:
    return tilteast(tiltsouth(tiltwest(tiltnorth(grid))))


def calc_weigth(grid: tuple[str, ...]) -> int:
    weight = 0
    for i, line in enumerate(reversed(grid), start=0):
        weight += i * Counter(line)["O"]
    return weight


def solution1(grid: tuple[str, ...]) -> int:
    new_grid = tiltnorth(grid)
    return calc_weigth(new_grid)


def solution2(grid: tuple[str, ...]) -> int:
    grids = defaultdict(lambda: [])
    cycle_len, stop_cycle = 0, -1
    new_grid = grid
    for cycle in range(1000000000):
        new_grid = tiltcycle(new_grid)

        if new_grid in grids and len(grids[new_grid]) > 1 and cycle_len == 0:
            repeat_cycle_start = grids[new_grid][1]
            cycle_len = repeat_cycle_start - grids[new_grid][0]
            rest = (1000000000 - repeat_cycle_start) % cycle_len
            # plausi check
            assert (1000000000 - (repeat_cycle_start + rest)) % cycle_len == 0
            stop_cycle = repeat_cycle_start + rest + cycle_len - 1

        grids[new_grid] += [cycle]
        if cycle == stop_cycle:
            # from here on it would just repeat up to 1000000000, so we can stop
            break

    return calc_weigth(new_grid)


def main() -> tuple[int, int]:
    lines = parse_input(get_input(Path(__file__).parent / "input01.txt"))
    return solution1(lines), solution2(lines)


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")
