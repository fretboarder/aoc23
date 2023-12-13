from collections import Counter
from functools import cache
from pathlib import Path
from pprint import pp
from typing import NamedTuple

from aoc23.support import get_input


class Arrangement(NamedTuple):
    pattern: str
    mutable_pos: list[int]
    mask: int
    expo: int
    springs: list[int]


def generate_patterns(a: Arrangement) -> int:
    pp(f"processing arrangement {a.pattern}")
    matchcnt = 0
    for number in range(2**a.expo):
        fmt = "0{}b".format(a.expo)
        # pp(f"{number:{fmt}}")
        ptn = list(a.pattern)
        for rightshift in range(a.expo - 1, -1, -1):
            char = "#" if number >> rightshift & 1 == 1 else "."
            ptn[a.mutable_pos[a.expo - 1 - rightshift]] = char
        if [len(c) for c in "".join(ptn).split(".") if len(c) > 0] == a.springs:
            matchcnt += 1
    pp(f"processing arrangement {a.springs} = {matchcnt}")
    return matchcnt


def parse_line(line: str) -> Arrangement:
    arr, cnt = line.split()
    springs = [int(c) for c in cnt.split(",")]
    mutable_pos, mask = [], ""

    for i, c in enumerate(arr):
        mask += "1" if c == "?" else "0"
        mutable_pos += [i] if c == "?" else []
    return Arrangement(arr, mutable_pos, int(mask, 2), Counter(mask)["1"], springs)


def parse_line2(line: str) -> Arrangement:
    arr, cnt = line.split()
    arr = "?".join([arr for _ in range(5)])
    cnt = ",".join([cnt for _ in range(5)])
    springs = [int(c) for c in cnt.split(",")]
    mutable_pos, mask = [], ""

    for i, c in enumerate(arr):
        mask += "1" if c == "?" else "0"
        mutable_pos += [i] if c == "?" else []
    return Arrangement(arr, mutable_pos, int(mask, 2), Counter(mask)["1"], springs)


@cache
def gen_pattern_rec(pattern: str, groups: tuple[int]) -> int:  # noqa: PLR0911
    if len(pattern) == 0:  # base case: no more pattern left
        return 1 if len(groups) == 0 else 0
    match pattern[0]:
        case ".":  # nothing to do, continue with remaining pattern
            return gen_pattern_rec(pattern[1:], groups)
        case "?":  # replace initial "?" by "." and "?"
            return gen_pattern_rec(f".{pattern[1:]}", groups) + gen_pattern_rec(
                f"#{pattern[1:]}", groups
            )
        case "#":
            if (  # base cases
                len(groups) == 0  # no more groups left
                or len(pattern) < groups[0]  # remaining pattern smaller than next group
                or any(c == "." for c in pattern[0 : groups[0]])  # e.g. "##.???" (3,1)
            ):
                # e.g. "##" (,)
                return 0
            if len(groups) > 1:
                if len(pattern) < groups[0] + 1 or pattern[groups[0]] == "#":
                    return 0
                # e.g. "##.???" (2,1)
                # -> "???" (1,)
                return gen_pattern_rec(pattern[groups[0] + 1 :], groups[1:])

            # e.g. "##.???" (2,)
            # -> ".???" (,)
            return gen_pattern_rec(pattern[groups[0] :], groups[1:])
    msg = "you shouldn't end up here at all!"
    raise Exception(msg)


def solution(arr: list[Arrangement]) -> int:
    results = [gen_pattern_rec(a.pattern, tuple(a.springs)) for a in arr]
    return sum(results)


def main() -> tuple[int, int]:
    arr = get_input(Path(__file__).parent / "input01.txt", parse_line)
    arr2 = get_input(Path(__file__).parent / "input01.txt", parse_line2)
    return solution(arr), solution(arr2)


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")
