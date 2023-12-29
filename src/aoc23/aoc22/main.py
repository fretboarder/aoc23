from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import reduce
from itertools import chain
from math import inf
from pathlib import Path
from pprint import pp
from typing import Iterable

from aoc23.support import get_input

Grid = list[list[int]]


def parse_line(lineno: int, line: str) -> Brick:
    e = line.replace("~", ",").split(",")
    return Brick(lineno, *[int(n) for n in e])


@dataclass(unsafe_hash=True, slots=True)
class Brick:
    n: int = field(hash=True)  # actually just the line number as unique id
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int

    def clone(self) -> Brick:
        return Brick(self.n, self.x1, self.y1, self.z1, self.x2, self.y2, self.z2)

    @property
    def height(self) -> int:
        return self.z2 - self.z1

    def overlap(self, other: Brick) -> bool:
        my_min_x, my_max_x = (
            (self.x1, self.x2) if self.x1 < self.x2 else (self.x2, self.x1)
        )
        my_min_y, my_max_y = (
            (self.y1, self.y2) if self.y1 < self.y2 else (self.y2, self.y1)
        )
        their_min_x, their_max_x = (
            (other.x1, other.x2) if other.x1 < other.x2 else (other.x2, other.x1)
        )
        their_min_y, their_max_y = (
            (other.y1, other.y2) if other.y1 < other.y2 else (other.y2, other.y1)
        )

        x_ov = y_ov = False
        if (
            my_min_x <= their_min_x <= my_max_x or my_min_x <= their_max_x <= my_max_x
        ) or (
            their_min_x <= my_min_x <= their_max_x
            or their_min_x <= my_max_x <= their_max_x
        ):
            x_ov = True

        if (
            my_min_y <= their_min_y <= my_max_y or my_min_y <= their_max_y <= my_max_y
        ) or (
            their_min_y <= my_min_y <= their_max_y
            or their_min_y <= my_max_y <= their_max_y
        ):
            y_ov = True

        return x_ov and y_ov


def resting_on(bottom: Iterable[Brick], brick: Brick) -> set[Brick]:
    rests_on = sorted(
        [base for base in bottom if brick.overlap(base)],
        key=lambda b: b.z2,
        reverse=True,
    )
    if not rests_on:
        return set()

    return set(
        reduce(
            lambda acc, cur: [*acc, cur] if cur.z2 == acc[-1].z2 else acc,
            rests_on,
            [rests_on[0]],
        )
    )


def pulldown(all_bricks: dict[int, list[Brick]]) -> tuple[dict[Brick, set[Brick]], int]:
    """Return the number of bricks that could be disintegrated."""
    processed = set()  # set(_bottom)
    remaining = deque(chain(*list(all_bricks.values())))
    # key brick is resting on set of other bricks
    resting_map: dict[Brick, set[Brick]] = defaultdict(set)

    bricks_dropped = 0

    while remaining:
        brick = remaining.popleft()
        rests_on = resting_on(processed, brick)
        processed.add(brick)
        if rests_on:
            top_z = next(iter(rests_on)).z2
            resting_map[brick] = rests_on
        else:
            # doesn't rest on any other brick, drop to base level
            top_z = 0

        if (drop_offs := brick.z1 - 1 - top_z) > 0:
            new_z1, new_z2 = brick.z1 - drop_offs, brick.z2 - drop_offs
            all_bricks[brick.z1].remove(brick)
            all_bricks[new_z1].append(brick)
            brick.z1, brick.z2 = new_z1, new_z2
            bricks_dropped += 1

    return resting_map, bricks_dropped


def get_disintegratable(
    resting_map: dict[Brick, set[Brick]], all_bricks: dict[int, list[Brick]]
) -> set[Brick]:
    # preset list with all bricks
    can_dis = {b for _, bricklist in all_bricks.items() for b in bricklist}
    # identify those which cannot be disintegrated
    not_dis = {next(iter(rs)) for rs in resting_map.values() if len(rs) == 1}
    return can_dis - not_dis


def solution1(bricks: list[Brick]) -> int:
    layers: dict[int, list[Brick]] = defaultdict(list)
    for b in bricks:
        layers[b.z1].append(b)

    resting_map = pulldown(layers)[0]
    return len(get_disintegratable(resting_map, layers))


def get_dim(bricks: Iterable[Brick]) -> tuple[int, int]:
    min_x = min_y = inf
    max_x = max_y = -inf
    for b in bricks:
        min_x = min(min_x, b.x1, b.x2)
        min_y = min(min_y, b.y1, b.y2)
        max_x = max(max_x, b.x1, b.x2)
        max_y = max(max_y, b.y1, b.y2)

    return int(max_x - min_x), int(max_y - min_y)


def update_grid(grid: Grid, b: Brick) -> int:
    def row_max(row: int, r1: int, r2: int) -> int:
        return max([grid[row][col] for col in range(r1, r2 + 1)])

    def col_max(col: int, r1: int, r2: int) -> int:
        return max([grid[row][col] for row in range(r1, r2 + 1)])

    def update_row(row: int, r1: int, r2: int, value: int) -> None:
        for col in range(r1, r2 + 1):
            grid[row][col] = value

    def update_col(col: int, r1: int, r2: int, value: int) -> None:
        for row in range(r1, r2 + 1):
            grid[row][col] = value

    min_x, max_x = (b.x1, b.x2) if b.x1 <= b.x2 else (b.x2, b.x1)
    min_y, max_y = (b.y1, b.y2) if b.y1 <= b.y2 else (b.y2, b.y1)
    max_z = (
        row_max(b.y1, min_x, max_x) if min_y == max_y else col_max(b.x1, min_y, max_y)
    )
    new_z = max_z + 1 + b.height

    if min_y == max_y:  # horizontal
        update_row(b.y1, min_x, max_x, new_z)
    else:  # vertical or 1 cube
        update_col(b.x1, min_y, max_y, new_z)
    # return the number of units dropped
    return b.z1 - (max_z + 1)


def drop(grid: Grid, sorted_bricks: Iterable[Brick]) -> int:
    return sum(1 if update_grid(grid, brick) > 0 else 0 for brick in sorted_bricks)


def solution2(bricks: list[Brick]) -> int:
    """Bricks is already compacted and must be sorted."""
    width, height = get_dim(bricks)
    return sum(
        drop(
            [[0 for _ in range(width + 1)] for _ in range(height + 1)],
            bricks[:i] + bricks[i + 1 :],
        )
        for i, _ in enumerate(bricks)
    )


def main() -> tuple[int, int]:
    lines = get_input(Path(__file__).parent / "input01.txt")
    blocks = sorted(
        [parse_line(i, line) for i, line in enumerate(lines, start=1)],
        key=lambda brck: brck.z1,
    )
    return solution1(blocks), solution2(sorted(blocks, key=lambda brck: brck.z1))


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")
