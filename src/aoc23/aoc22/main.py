from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import reduce
from itertools import chain
from pathlib import Path
from pprint import pp
from typing import Iterable

from aoc23.support import get_input


def parse_line(lineno: int, line: str) -> Brick:
    e = line.replace("~", ",").split(",")
    return Brick(lineno, *[int(n) for n in e])


@dataclass(unsafe_hash=True)
class Brick:
    n: int = field(hash=True)  # actually just the line number as unique id
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int

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


def pulldown(all_bricks: dict[int, list[Brick]]) -> int:
    """Return the number of bricks that could be disintegrated."""
    _bottom, *_remaining = list(all_bricks.values())
    processed = set(_bottom)
    remaining = deque(chain(*_remaining))
    resting_map: dict[Brick, set[Brick]] = defaultdict(set)

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

    # preset list with all bricks
    can_dis = {b for _, bricklist in all_bricks.items() for b in bricklist}
    # identify those which cannot be disintegrated
    not_dis = {next(iter(rs)) for rs in resting_map.values() if len(rs) == 1}
    return len(can_dis - not_dis)


def solution1(blocks: list[Brick]) -> int:
    layers = defaultdict(lambda: [])
    for b in blocks:
        layers[b.z1].append(b)
    return pulldown(layers)


def solution2(blocks: list[Brick]) -> int:
    return 0


def main() -> tuple[int, int]:
    lines = get_input(Path(__file__).parent / "input01.txt")
    blocks = sorted(
        [parse_line(i, line) for i, line in enumerate(lines)], key=lambda brck: brck.z1
    )

    return solution1(blocks), solution2(blocks)


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")
