from __future__ import annotations

from collections import deque
from enum import Enum
from pathlib import Path
from pprint import pp
from typing import Final, NamedTuple

from aoc23.support import get_input

Grid = list[str]


class Pos(NamedTuple):
    col: int  # x
    row: int  # y


class Direction(Enum):
    LEFT = Pos(-1, 0)
    RIGHT = Pos(1, 0)
    UP = Pos(0, -1)
    DOWN = Pos(0, 1)


DIRMAP: Final = {
    Direction.LEFT: {
        "|": [Direction.UP, Direction.DOWN],
        "/": [Direction.DOWN],
        "\\": [Direction.UP],
    },
    Direction.RIGHT: {
        "|": [Direction.UP, Direction.DOWN],
        "/": [Direction.UP],
        "\\": [Direction.DOWN],
    },
    Direction.UP: {
        "-": [Direction.LEFT, Direction.RIGHT],
        "/": [Direction.RIGHT],
        "\\": [Direction.LEFT],
    },
    Direction.DOWN: {
        "-": [Direction.LEFT, Direction.RIGHT],
        "/": [Direction.LEFT],
        "\\": [Direction.RIGHT],
    },
}


class Cell(NamedTuple):
    pos: Pos
    approached: Direction


def is_inside_grid(grid: Grid, pos: Pos) -> bool:
    return 0 <= pos.col < len(grid[0]) and 0 <= pos.row < len(grid)


def neighbor(pos: Pos, direction: Direction) -> Pos:
    return Pos(pos.col + direction.value.col, pos.row + direction.value.row)


def get_next_pos(
    grid: Grid, current_pos: Pos, flow_dir: Direction
) -> tuple[tuple[Pos, Direction], ...]:
    current_symbol = grid[current_pos.row][current_pos.col]
    return tuple(
        [
            (neighbor(current_pos, fd), fd)
            for fd in DIRMAP[flow_dir].get(current_symbol, [flow_dir])
        ]
    )


def bfs(
    grid: Grid,
    initial_pos: Pos,
    flow_dir: Direction,
) -> set[tuple[Pos, Direction]]:
    frontier: deque[tuple[Pos, Direction]] = deque([(initial_pos, flow_dir)])
    visited: set[tuple[Pos, Direction]] = set()
    while frontier:
        current_pos, flow_dir = frontier.popleft()  # get the next position
        if (current_pos, flow_dir) in visited:  # skip, if we've been there
            continue

        visited.add((current_pos, flow_dir))  # add to local_cache
        for pos, d in get_next_pos(grid, current_pos, flow_dir):
            if is_inside_grid(grid, pos):
                frontier.append((pos, d))

    return visited


def solution1(grid: Grid) -> int:
    return len({pos for pos, _ in bfs(grid, Pos(0, 0), Direction.RIGHT)})


def solution2(grid: Grid) -> int:
    energized = 0

    p = [(Pos(0, row), Direction.RIGHT) for row in range(len(grid) - 1)]
    p += [(Pos(len(grid[0]) - 1, row), Direction.LEFT) for row in range(len(grid) - 1)]
    p += [(Pos(col, 0), Direction.DOWN) for col in range(len(grid[0]) - 1)]
    p += [(Pos(col, len(grid) - 1), Direction.UP) for col in range(len(grid[0]) - 1)]

    for start_pos, flow_dir in p:
        all_visited = bfs(grid, start_pos, flow_dir)
        visited = len({pos for pos, _ in all_visited})
        energized = max(energized, visited)

    return energized


def main() -> tuple[int, int]:
    lines = get_input(Path(__file__).parent / "input01.txt")
    return solution1(lines), solution2(lines)


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")  # check main2.py
