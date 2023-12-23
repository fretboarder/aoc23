from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
from pprint import pp
from sys import setrecursionlimit
from typing import NamedTuple

from aoc23.support import get_input


class Pos(NamedTuple):
    x: int  # x
    y: int  # y


Tree = dict[Pos, list[Pos]]

en = enumerate


def parse_maze(lines: list[str], honor_slopes: bool) -> Tree:
    grid = [list(row) for row in lines]
    ndict = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    positions = (
        Pos(x, y) for y, line in en(lines) for x, char in en(line) if char in ".<>^v"
    )
    tree: Tree = defaultdict(lambda: [])
    for p in positions:
        char = grid[p.y][p.x]
        if honor_slopes and char in ndict:
            offs_row, offs_col = ndict[char]
            tree[p].append(Pos(p.x + offs_col, p.y + offs_row))
        else:
            for offs_row, offs_col in ndict.values():
                nb = Pos(p.x + offs_col, p.y + offs_row)
                if (
                    0 <= nb.y < len(grid)
                    and 0 <= nb.x <= len(grid[0])
                    and grid[nb.y][nb.x] != "#"
                ):
                    tree[p].append(nb)

    return tree


def dfs_rec(tree: Tree, start: Pos, stop: Pos, visited: set[Pos]) -> int:
    steps = 0
    frontier = deque([(start, steps)])
    while frontier:
        current, steps = frontier.pop()
        if current == stop:
            return steps

        visited.add(current)

        unvis_neighbors = [n for n in tree[current] if n not in visited]
        if len(unvis_neighbors) == 1:
            frontier.append((unvis_neighbors[0], steps + 1))
        elif len(unvis_neighbors) > 1:
            # on a branching point, recursively start a new dfs
            sub_res = [
                1 + dfs_rec(tree, n, stop, set(visited)) for n in unvis_neighbors
            ]
            steps += max(sub_res)

    return steps


def solution1(tree: Tree, start: Pos, stop: Pos) -> int:
    visited: set[Pos] = set()
    return dfs_rec(tree, start, stop, visited)


def solution2(tree: Tree, start: Pos, stop: Pos) -> int:
    return 0


def main() -> tuple[int, int]:
    lines = get_input(Path(__file__).parent / "input01.txt")
    tree1, tree2 = (parse_maze(lines, slope) for slope in (True, False))
    start, stop = Pos(lines[0].index("."), 0), Pos(lines[-1].index("."), len(lines) - 1)
    return solution1(tree1, start, stop), solution2(tree2, start, stop)


if __name__ == "__main__":
    setrecursionlimit(10000)
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")
