from __future__ import annotations

from math import inf
from pathlib import Path
from pprint import pp
from typing import Callable, NamedTuple

from aoc23.support import get_input

Grid = list[list[str]]


class Pos(NamedTuple):
    col: int  # x
    row: int  # y


OFFSETS = {
    "R": Pos(1, 0),  # x, y
    "D": Pos(0, 1),  # x, y
    "L": Pos(-1, 0),  # x, y
    "U": Pos(0, -1),  # x, y
}


DIRS = {"0": "R", "1": "D", "2": "L", "3": "U"}


def decode_line2(line: str) -> tuple[str, int]:
    _, _, instr = line.split(" ")
    return DIRS[instr[-2]], int(instr[2:-2], 16)


def decode_line1(line: str) -> tuple[str, int]:
    direction, cnt, _ = line.split(" ")
    return direction, int(cnt)


def parse_input(
    lines: list[str], decode: Callable[[str], tuple[str, int]]
) -> list[Pos]:
    vertices = [Pos(0, 0)]
    max_row, max_col = -inf, -inf
    min_col, min_row = inf, inf
    pos = vertices[-1]
    for line in lines:
        direction, cnt = decode(line)
        if direction in ("L", "R"):
            offs = OFFSETS[direction].col
            vertices.append(Pos(pos.col + (offs * cnt), pos.row))
        else:
            offs = OFFSETS[direction].row
            vertices.append(Pos(pos.col, pos.row + (offs * cnt)))

        max_col = int(max(max_col, vertices[-1].col))
        max_row = int(max(max_row, vertices[-1].row))
        min_col = int(min(min_col, vertices[-1].col))
        min_row = int(min(min_row, vertices[-1].row))
        pos = vertices[-1]

    # shift positions to origin for shoelace to work
    xoffs, yoffs = int(abs(min(0, min_col))), int(abs(min(0, min_row)))
    new_edges: list[Pos] = []
    for e in vertices:
        pos = Pos(e.col + xoffs, e.row + yoffs)
        new_edges.append(pos)

    return new_edges


def perimeter(vertices: list[Pos]) -> int:
    dist, v0 = 0, vertices[0]
    for v1 in vertices[1:]:
        # one diff is always zero in our case
        dist += abs(v1.col - v0.col) + abs(v1.row - v0.row)
        v0 = v1
    return dist


def shoelace(vertices: list[Pos]) -> float:
    def cp(a: Pos, b: Pos) -> int:
        return (a.row + b.row) * (a.col - b.col)

    total = sum(cp(vertices[i], vertices[(i + 1)]) for i, _ in enumerate(vertices[:-1]))
    return abs(total) / 2


def solution(lines: list[str], decode: Callable[[str], tuple[str, int]]) -> int:
    vertices = parse_input(lines, decode)
    A = shoelace(vertices)  # shoelace formula to get the interior
    return int(A + perimeter(vertices) / 2 + 1)  # Pick's theorem


def main() -> tuple[int, int]:
    lines = get_input(Path(__file__).parent / "input01.txt")
    return solution(lines, decode_line1), solution(lines, decode_line2)


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")  # check main2.py
