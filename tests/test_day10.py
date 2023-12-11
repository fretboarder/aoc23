from typing import Callable

import pytest
from aoc23.aoc10 import main

g1 = [
    "..|..",
    ".-S-.",
    "..|..",
]


@pytest.fixture()
def grid() -> Callable:
    def get(g1: main.Grid, startsym: str) -> list[str]:
        g = [*g1]
        g[1] = g1[1].replace("S", startsym)
        return g

    return get


@pytest.mark.parametrize(
    ("startsym", "matches"),
    [("S", 4), ("|", 2), ("-", 2), ("F", 2), ("7", 2), ("L", 2), ("J", 2)],
)
def test_valid_neighbor1(grid, startsym, matches):
    res = [
        main.is_valid_neighbor(grid(g1, startsym), main.Pos(2, 1), d) for d in main.DIRS
    ]
    assert len([r for r, _ in res if r]) == matches


g2 = [
    "..F..",
    ".LS7.",
    "..J..",
]


@pytest.mark.parametrize(
    ("startsym", "matches"),
    [("S", 4), ("|", 2), ("-", 2), ("F", 2), ("7", 2), ("L", 2), ("J", 2)],
)
def test_valid_neighbor2(grid, startsym, matches):
    res = [
        main.is_valid_neighbor(grid(g2, startsym), main.Pos(2, 1), d) for d in main.DIRS
    ]
    assert len([r for r, _ in res if r]) == matches


g3 = [
    "..L..",
    ".JSF.",
    "..7..",
]


@pytest.mark.parametrize(
    ("startsym", "matches"),
    [("S", 0), ("|", 0), ("-", 0), ("F", 0), ("7", 0), ("L", 0), ("J", 0)],
)
def test_valid_neighbor3(grid, startsym, matches):
    res = [
        main.is_valid_neighbor(grid(g3, startsym), main.Pos(2, 1), d) for d in main.DIRS
    ]
    assert len([r for r, _ in res if r]) == matches


g4 = [
    "..7..",
    ".FSJ.",
    "..L..",
]


@pytest.mark.parametrize(
    ("startsym", "matches"),
    [("S", 4), ("|", 2), ("-", 2), ("F", 2), ("7", 2), ("L", 2), ("J", 2)],
)
def test_valid_neighbor4(grid, startsym, matches):
    res = [
        main.is_valid_neighbor(grid(g4, startsym), main.Pos(2, 1), d) for d in main.DIRS
    ]
    assert len([r for r, _ in res if r]) == matches


g5 = [
    "..F..",
    ".FSF.",
    "..F..",
]


@pytest.mark.parametrize(
    ("startsym", "matches"),
    [("S", 2), ("|", 1), ("-", 1), ("F", 0), ("7", 1), ("L", 1), ("J", 2)],
)
def test_valid_neighbor5(grid, startsym, matches):
    res = [
        main.is_valid_neighbor(grid(g5, startsym), main.Pos(2, 1), d) for d in main.DIRS
    ]
    assert len([r for r, _ in res if r]) == matches
