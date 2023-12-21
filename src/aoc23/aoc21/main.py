from __future__ import annotations

from enum import Enum
from pathlib import Path
from pprint import pp
from typing import NamedTuple

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


def print_grid(grid: Grid) -> None:
    for row in grid:
        pp(row)


def make_grid(grid: Grid, steps: set[Pos]) -> Grid:
    g = [list(row) for row in grid]

    for s in steps:
        g[s.row][s.col] = "O"

    return ["".join(row) for row in g]


def get_start_pos(grid: Grid, char: str) -> Pos:
    for r, row in enumerate(grid):
        if (c := row.find(char)) > -1:
            return Pos(c, r)
    msg = f"{char} not found in grid"
    raise ValueError(msg)


def is_inside_grid(grid: Grid, pos: Pos) -> bool:
    return 0 <= pos.col < len(grid[0]) and 0 <= pos.row < len(grid)


def neighbor(pos: Pos, direction: Direction) -> Pos:
    return Pos(pos.col + direction.value.col, pos.row + direction.value.row)


def is_valid_neighbor(grid: Grid, pos: Pos, direction: Direction) -> bool:
    n = neighbor(pos, direction)
    return is_inside_grid(grid, n) and (grid[n.row][n.col] not in ("S", "#"))


def get_neighbors(grid: Grid, current_pos: Pos) -> tuple[Pos, ...]:
    return tuple(
        [
            neighbor(current_pos, fd)
            for fd in Direction
            if is_valid_neighbor(grid, current_pos, fd)
        ]
    )


def move(grid: Grid, initial_pos: Pos, step_count: int) -> set[tuple[int, Pos]]:
    # for every round, move away from every plot 1 step
    visited: set[tuple[int, Pos]] = {(0, initial_pos)}
    for _ in range(step_count):
        local_stack: set[tuple[int, Pos]] = set()
        for steps, pos in visited:
            reachable_neighbors = {
                (steps + 1, n) for n in set(get_neighbors(grid, pos))
            }
            local_stack |= reachable_neighbors
        visited |= set(local_stack)
    return visited


def solution1(grid: Grid) -> int:
    steps = 64
    start = get_start_pos(grid, "S")
    visited = move(grid, start, steps)
    g = make_grid(grid, {v for s, v in visited if s == steps})
    return len({v for s, v in visited if s == steps}) + 1


def cmod(x: complex, modulo: int) -> complex:
    return complex(x.real % modulo, x.imag % modulo)


def calculate(repetitions: int, t1: int, t2: int, t3: int) -> int:
    return t1 + repetitions * (t2 - t1 + (repetitions - 1) * (t3 - t2 - t2 + t1) // 2)


def solution2(grid: Grid) -> int:
    goal, modulo, steps, sol1 = 26501365, 131, 64, 0

    # positions of "." and "S", coordinates represented as complex
    positions: dict[complex, str] = {
        i + j * 1j: c for i, r in enumerate(grid) for j, c in enumerate(r) if c in ".S"
    }

    done: list[int] = []
    todo = {x for x in positions if positions[x] == "S"}

    for s in range(3 * modulo):
        # if s == steps:
        #     sol1 = len(todo)  # noqa: ERA001
        if s % modulo == steps + 1:
            done.append(len(todo))

        todo = {
            t + offset  # that's the new positions
            for offset in (1, -1, 1j, -1j)
            for t in todo
            if cmod(t + offset, modulo) in positions
        }

    return calculate(goal // modulo, *done)


def main() -> tuple[int, int]:
    lines = get_input(Path(__file__).parent / "input01.txt")
    return solution1(lines), solution2(lines)


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")  # check main2.py
