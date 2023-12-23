from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
from pprint import pp
from sys import setrecursionlimit
from typing import NamedTuple

from aoc23.support import get_input


class Pos(NamedTuple):
    col: int  # x
    row: int  # y


Tree = dict[Pos, list[Pos]]


def parse_maze(lines: list[str], honor_slopes: bool) -> Tree:
    if honor_slopes:
        grid = [list(row) for row in lines]
    else:
        grid = [
            list(
                row.replace("<", ".")
                .replace(">", ".")
                .replace("v", ".")
                .replace("^", ".")
            )
            for row in lines
        ]

    ndict = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    positions = (
        Pos(col, row)
        for row, line in enumerate(lines)
        for col, char in enumerate(line)
        if char in ".<>^v"
    )
    tree: Tree = defaultdict(lambda: [])
    for pos in positions:
        char = grid[pos.row][pos.col]
        if char in ndict:
            offs_row, offs_col = ndict[char]
            tree[pos].append(Pos(pos.col + offs_col, pos.row + offs_row))
        else:
            for offs_row, offs_col in ndict.values():
                neighbor = Pos(pos.col + offs_col, pos.row + offs_row)
                if (
                    0 <= neighbor.row < len(grid)
                    and 0 <= neighbor.col <= len(grid[0])
                    and grid[neighbor.row][neighbor.col] != "#"
                ):
                    tree[pos].append(neighbor)

    return tree


def dfs_rec(tree: Tree, start: Pos, stop: Pos, visited: set[Pos]) -> int:
    frontier = deque([(start, 0)])
    steps = 0
    while frontier:
        current, steps = frontier.pop()
        if current == stop:
            return steps

        visited.add(current)

        unvis_neighbors = [n for n in tree[current] if n not in visited]
        if len(unvis_neighbors) == 1:
            frontier.append((unvis_neighbors[0], steps + 1))
        elif len(unvis_neighbors) > 1:
            sub_res = [
                1 + dfs_rec(tree, n, stop, set(visited)) for n in unvis_neighbors
            ]
            steps += max(sub_res)

    return steps


def solution1(tree: Tree, start: Pos, stop: Pos) -> int:
    visited: set[Pos] = set()
    res = dfs_rec(tree, start, stop, visited)
    return res


def solution2(tree: Tree, start: Pos, stop: Pos) -> int:
    return 0


def main() -> tuple[int, int]:
    lines = get_input(Path(__file__).parent / "ex01.txt")
    tree1, tree2 = (parse_maze(lines, slope) for slope in (True, False))
    start, stop = Pos(lines[0].index("."), 0), Pos(lines[-1].index("."), len(lines) - 1)
    return solution1(tree1, start, stop), solution2(tree2, start, stop)


if __name__ == "__main__":
    setrecursionlimit(10000)
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")
