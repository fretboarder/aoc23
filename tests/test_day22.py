from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import NamedTuple

import pytest
from aoc23.aoc22.main import Brick, get_dim, parse_line, pulldown

#             x3, y3
#               |
#  x1, y1 ------+------ x2, y1
#               |
#             x3, y4


@pytest.mark.parametrize(
    "brick",
    [
        Brick(1, 0, 2, 1, 1, 2),
        Brick(1, 1, 2, 1, 2, 2),
        Brick(0, 1, 2, 1, 1, 2),
        Brick(1, 1, 2, 2, 1, 2),
        Brick(0, 1, 2, 2, 1, 2),
        Brick(1, 0, 2, 1, 2, 2),
    ],
)
def test_overlap(brick: Brick):
    b1 = Brick(1, 1, 1, 1, 1, 1)
    assert b1.overlap(brick)
    assert brick.overlap(b1)


@pytest.mark.parametrize(
    "x, y",
    [
        (0, 0),
        (1, 0),
        (2, 0),
        (0, 1),
        (2, 1),
        (0, 2),
        (1, 2),
        (2, 2),
    ],
)
def test_no_overlap(x, y):
    b1 = Brick(1, 1, 1, 1, 1, 1)
    assert not b1.overlap(Brick(x, y, 1, x, y, 1))
    assert not Brick(x, y, 1, x, y, 1).overlap(b1)


def test_no_overlap1():
    assert not Brick(0, 3, 1, 0, 3, 2).overlap(Brick(3, 3, 3, 4, 3, 3))


def test_parse_line():
    lines = [
        "0,3,1~0,3,2",
        "0,0,4~0,3,4",
        "0,0,1~2,0,1",
        "3,3,3~4,3,3",
        "0,2,2~0,2,2",
        "4,1,1~4,3,1",
    ]
    bricks = sorted([parse_line(line) for line in lines], key=lambda b: b.z1)

    assert bricks == [
        Brick(x1=0, y1=3, z1=1, x2=0, y2=3, z2=2),
        Brick(x1=0, y1=0, z1=1, x2=2, y2=0, z2=1),
        Brick(x1=4, y1=1, z1=1, x2=4, y2=3, z2=1),
        Brick(x1=0, y1=2, z1=2, x2=0, y2=2, z2=2),
        Brick(x1=3, y1=3, z1=3, x2=4, y2=3, z2=3),
        Brick(x1=0, y1=0, z1=4, x2=0, y2=3, z2=4),
    ]
    assert get_dim(bricks) == (0, 0, 4, 3)

    layers = defaultdict(lambda: [])
    for b in bricks:
        layers[b.z1].append(b)

    for i in list(layers.keys())[1:]:
        pulldown(i, layers)
    assert False
