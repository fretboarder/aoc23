from collections import deque
from enum import Enum
from pathlib import Path
from pprint import pp
from typing import NamedTuple

from aoc23.support import get_input


class Pos(NamedTuple):
    col: int  # x
    row: int  # y


Grid = list[str]


class Direction(Enum):
    WEST = Pos(-1, 0)
    EAST = Pos(1, 0)
    NORTH = Pos(0, -1)
    SOUTH = Pos(0, 1)


DIRS = {
    Direction.EAST: Pos(1, 0),
    Direction.WEST: Pos(-1, 0),
    Direction.NORTH: Pos(0, -1),
    Direction.SOUTH: Pos(0, 1),
}

VALID_NEIGHBORS = {
    Direction.NORTH: [
        ("|", "|"),
        ("|", "F"),
        ("|", "7"),
        ("L", "|"),
        ("L", "7"),
        ("L", "F"),
        ("J", "|"),
        ("J", "7"),
        ("J", "F"),
        ("S", "|"),
        ("S", "7"),
        ("S", "F"),
    ],
    Direction.SOUTH: [
        ("|", "|"),
        ("|", "L"),
        ("|", "J"),
        ("F", "|"),
        ("F", "L"),
        ("F", "J"),
        ("7", "|"),
        ("7", "L"),
        ("7", "J"),
        ("S", "|"),
        ("S", "L"),
        ("S", "J"),
    ],
    Direction.WEST: [
        ("-", "-"),
        ("-", "F"),
        ("-", "L"),
        ("7", "-"),
        ("7", "F"),
        ("7", "L"),
        ("J", "-"),
        ("J", "F"),
        ("J", "L"),
        ("S", "-"),
        ("S", "F"),
        ("S", "L"),
    ],
    Direction.EAST: [
        ("-", "-"),
        ("-", "7"),
        ("-", "J"),
        ("F", "-"),
        ("F", "J"),
        ("F", "7"),
        ("L", "-"),
        ("L", "J"),
        ("L", "7"),
        ("S", "-"),
        ("S", "J"),
        ("S", "7"),
    ],
}


def is_valid_neighbor(
    grid: Grid, current_pos: Pos, neighbor: Direction
) -> tuple[bool, Pos]:
    sym = grid[current_pos.row][current_pos.col]
    new_pos = Pos(
        current_pos.col + DIRS[neighbor].col, current_pos.row + DIRS[neighbor].row
    )
    if new_pos.col < len(grid[0]) and new_pos.row < len(grid):
        neighbor_sym = grid[new_pos.row][new_pos.col]
        return (sym, neighbor_sym) in VALID_NEIGHBORS[neighbor], new_pos
    return False, new_pos


def get_initial_pos(grid: Grid) -> Pos:
    for r, row in enumerate(grid):
        if (c := row.find("S")) != -1:
            return Pos(c, r)
    msg = "grid doesn't seem to have a starting position"
    raise ValueError(msg)


def get_starting_directions(
    grid: Grid, initial_pos: Pos
) -> tuple[Direction, Direction]:
    dirs = [d for d in Direction if is_valid_neighbor(grid, initial_pos, d)[0]]
    if len(dirs) == 2:  # noqa: PLR2004
        return dirs[0], dirs[1]
    msg = f"Expected to find 2 directions, found {len(dirs)}"
    raise ValueError(msg)


def bfs(grid: Grid, initial_pos: Pos, initial_dir: Direction) -> list[Pos]:
    steps = 1
    visited = {initial_pos}

    positions: list[Pos] = []
    _, new_pos = is_valid_neighbor(grid, initial_pos, initial_dir)

    frontier = deque([(new_pos, steps)])

    while frontier:
        current_pos, steps = frontier.popleft()
        if current_pos in visited:
            continue

        visited.add(current_pos)
        for direction in DIRS:
            valid_neighbor, new_pos = is_valid_neighbor(grid, current_pos, direction)
            if new_pos not in visited and valid_neighbor:
                positions.append(new_pos)
                frontier.append((new_pos, steps + 1))

    return positions


def solution1(grid: Grid) -> int:
    steps = [
        bfs(grid, get_initial_pos(grid), d)
        for d in get_starting_directions(grid, get_initial_pos(grid))
    ]

    for i, (p1, p2) in enumerate(zip(*steps), start=2):
        if p1 == p2:
            break

    return i


def main() -> tuple[int, int]:
    lines = get_input(Path(__file__).parent / "ex01.txt")
    return solution1(lines), 0


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")  # check main2.py
