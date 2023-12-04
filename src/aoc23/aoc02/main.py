import re
from functools import reduce
from pathlib import Path
from typing import TypedDict

from aoc23.support import get_input


class Roll(TypedDict):
    red: int
    green: int
    blue: int


EmptyRoll = Roll(red=0, green=0, blue=0)


class Game(TypedDict):
    id: int
    rolls: list[Roll]


def parse_line(line: str) -> Game:
    matches = re.findall(r"Game (\d+):(.*)", line)
    gid, cubesets = matches[0][0], matches[0][1].split(";")
    g = Game(id=int(gid), rolls=[])
    for cubeset in cubesets:
        cnt_cols = re.findall(r"(?P<cnt>\d+) (?P<col>\w+)", cubeset)
        roll = Roll(**(EmptyRoll | dict([(col, int(cnt)) for cnt, col in cnt_cols])))
        g["rolls"].append(roll)
    return g


def game_possible(g: Game):
    return sum(
        [
            1
            for r in g["rolls"]
            if r["red"] <= 12 and r["green"] <= 13 and r["blue"] <= 14
        ]
    ) == len(g["rolls"])


def min_cubes(g: Game):
    def _reducer(rolls: Roll, next_roll: Roll):
        return Roll(
            red=max(rolls["red"], next_roll["red"]),
            green=max(rolls["green"], next_roll["green"]),
            blue=max(rolls["blue"], next_roll["blue"]),
        )

    return reduce(_reducer, g["rolls"], Roll(red=0, green=0, blue=0))


def roll_power(r: Roll) -> int:
    return max(1, r["red"]) * max(1, r["green"]) * max(1, r["blue"])


def main[A, B]() -> tuple[A, B]:
    lines1 = get_input(Path(__file__).parent / "input01.txt")
    games = [parse_line(l) for l in lines1]
    return sum([g["id"] for g in games if game_possible(g)]), sum(
        [roll_power(min_cubes(g)) for g in games]
    )


if __name__ == "__main__":
    sol1, sol2 = main()
    # Solution 1: 3059
    print("Solution 1", sol1)
    # Solution 2: 65371
    print("Solution 2", sol2)
