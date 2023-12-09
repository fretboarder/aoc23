from pathlib import Path
from pprint import pp
from typing import Callable

from aoc23.support import get_input

History = list[list[int]]


def parse(line: str) -> list[int]:
    return [int(n) for n in line.split()]


def line_diffs(numbers: list[int]) -> list[int]:
    sums, n0 = [], numbers[0]
    for n in numbers[1:]:
        sums.append(n - n0)
        n0 = n
    return sums


def create_history(line: list[int]) -> History:
    def loop(acc: History, next_line: list[int]) -> History:
        if set(next_line) == {0}:
            return acc
        new_line = line_diffs(next_line)
        return loop([new_line] + acc, new_line)

    res = loop([line], line)
    return res


def extrap1(history: History) -> int:
    extrapolated = history[0][-1]
    for number_line in history[1:]:
        extrapolated += number_line[-1]
    return extrapolated


def extrap2(history: History) -> int:
    extrapolated = history[0][0]
    for number_line in history[1:]:
        extrapolated = number_line[0] - extrapolated
    return extrapolated


def solution(
    input_lines: list[list[int]], extrapolate: Callable[[History], int]
) -> int:
    all: list[int] = []
    for l in input_lines:
        all.append(extrapolate(create_history(l)))
    return sum(all)


def main() -> tuple[int, int]:
    lines = get_input(Path(__file__).parent / "input01.txt", parse)
    return solution(lines, extrap1), solution(lines, extrap2)


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")
