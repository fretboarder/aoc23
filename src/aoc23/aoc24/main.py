from __future__ import annotations

from itertools import combinations
from pathlib import Path
from pprint import pp
from typing import NamedTuple

from aoc23.support import get_input


class Pos(NamedTuple):
    x: float
    y: float


class Line(NamedTuple):
    p1: Pos
    p2: Pos


class Stone(NamedTuple):
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int


def parse_line(line: str) -> Stone:
    return Stone(*[int(i) for i in line.replace("@", ",").replace(" ", "").split(",")])


def intersection(s1: Stone, s2: Stone) -> Pos | None:
    """Calculates the intersection point of two lines."""
    l1 = Line(Pos(s1.x, s1.y), Pos(s1.x + s1.vx, s1.y + s1.vy))
    l2 = Line(Pos(s2.x, s2.y), Pos(s2.x + s2.vx, s2.y + s2.vy))

    # Check if the lines are parallel.
    m1 = (l1.p2.y - l1.p1.y) / (l1.p2.x - l1.p1.x)
    m2 = (l2.p2.y - l2.p1.y) / (l2.p2.x - l2.p1.x)
    if m1 == m2:  # parallel
        return None

    d1 = l1.p1.y - m1 * l1.p1.x
    d2 = l2.p1.y - m2 * l2.p1.x
    x_i = (d2 - d1) / (m1 - m2)
    y_i = (m1 * x_i) + d1
    return Pos(x_i, y_i)


def intersects_in_future(intersection: Pos, s1: Stone, s2: Stone) -> bool:
    in1 = abs(s1.x - intersection.x) + abs(s1.y - intersection.y)
    nx1 = abs(s1.x + s1.vx - intersection.x) + abs(s1.y + s1.vy - intersection.y)
    in2 = abs(s2.x - intersection.x) + abs(s2.y - intersection.y)
    nx2 = abs(s2.x + s2.vx - intersection.x) + abs(s2.y + s2.vy - intersection.y)
    return nx1 < in1 and nx2 < in2


border_min = 200000000000000
border_max = 400000000000000


def solution1(stones: list[Stone]) -> int:
    ints: set[tuple[Stone, Stone]] = set()
    for s1, s2 in combinations(stones, 2):
        if s1 == s2 or {s1, s2} in ints or {s2, s1} in ints:
            continue
        if (
            (i := intersection(s1, s2)) is not None
            and intersects_in_future(i, s1, s2)
            and border_min <= i.x <= border_max
            and border_min <= i.y <= border_max
        ):
            ints.add((s1, s2))
    return len(ints)


def solution2(stones: list[Stone]) -> int:
    return 0


def main() -> tuple[int, int]:
    stones = get_input(Path(__file__).parent / "input01.txt", parse_line)
    return solution1(stones), solution2(stones)


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")
