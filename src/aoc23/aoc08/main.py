import itertools
import re
from math import lcm
from pathlib import Path
from pprint import pp
from typing import Callable

from aoc23.support import get_input


def parse(lines: list[str]) -> tuple[str, dict[str, list[str]], list[str]]:
    inst = lines[0]
    start_nodes = []

    tree = dict()
    for line in lines[2:]:
        _key, _left, _right = re.findall(r"\w+", line)
        tree.update({_key: [_left, _right]})
        if _key.endswith("A"):
            start_nodes.append(_key)
    return inst, tree, start_nodes


def solution1(inst: str, m: dict, start_node: str, stop_crit: Callable) -> int:
    g = itertools.cycle(inst)
    next_node, steps = start_node, 0

    while not stop_crit(next_node) and (next_instruction := next(g)):
        left, right = m[next_node]
        next_node = left if next_instruction == "L" else right
        steps += 1
    return steps


def solution2(inst: str, m: dict, start_nodes: list[str]) -> int:
    results = []
    for start in start_nodes:
        s = solution1(inst, m, start, lambda n: n.endswith("Z"))
        results.append(s)
    return lcm(*results)


def main[A, B]() -> tuple[A, B]:
    inst, tree, start_nodes = parse(get_input(Path(__file__).parent / "input01.txt"))
    return solution1(inst, tree, "AAA", lambda n: n == "ZZZ"), solution2(
        inst, tree, start_nodes
    )


if __name__ == "__main__":
    sol1, sol2 = main()
    # Solution 1: 21389
    pp(f"Solution 1: {sol1}")
    # Solution 2: 21083806112641
    pp(f"Solution 2: {sol2}")
