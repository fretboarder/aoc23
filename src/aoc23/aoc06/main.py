import operator
import re
from dataclasses import dataclass
from functools import reduce
from pathlib import Path

from aoc23.support import get_input


@dataclass
class Race:
    time: int
    distance: int


def get_races_01(lines: list[str]) -> list[Race]:
    t = re.findall(r"\d+", lines[0])
    d = re.findall(r"\d+", lines[1])
    return [Race(int(fst), int(snd)) for fst, snd in zip(t, d)]


def get_races_02(lines: list[str]) -> list[Race]:
    t = int("".join(re.findall(r"\d+", lines[0])))
    d = int("".join(re.findall(r"\d+", lines[1])))
    return [Race(int(fst), int(snd)) for fst, snd in zip([t], [d])]


def calc_distance(hold_time: int, max_time: int) -> int:
    return (max_time - hold_time) * hold_time


# not really nice, but working
def solution(races: list[Race]):
    result = 1
    for race in races:
        result_count = 0
        q, r = divmod(race.time, 2)
        for hold_time in range(q + 1):
            if calc_distance(hold_time, race.time) > race.distance:
                result_count += 1
        result *= result_count * 2 - 1 + r
    return result


def main[A, B]() -> tuple[A, B]:
    lines = get_input(Path(__file__).parent / "input01.txt")
    return solution(get_races_01(lines)), solution(get_races_02(lines))


if __name__ == "__main__":
    sol1, sol2 = main()
    # Solution 1: 128700
    print("Solution 1", sol1)
    # Solution 2: 39594072
    print("Solution 2", sol2)
