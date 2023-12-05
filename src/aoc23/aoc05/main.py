import re
from pathlib import Path

from aoc23.support import get_input

sections = [
    "seed-to-soil map:",
    "soil-to-fertilizer map:",
    "fertilizer-to-water map:",
    "water-to-light map:",
    "light-to-temperature map:",
    "temperature-to-humidity map:",
    "humidity-to-location map:",
]

Seeds = list[int]
Ranges = list[list[int]]
Mappings = dict[str, Ranges]


def parse_input(lines: list[str]) -> tuple[Seeds, Mappings]:
    mappings = dict()
    seeds = [int(n) for n in re.findall(r"\d+", lines[0])]
    map_name = ""
    for l in lines[1:]:
        if not l:
            continue
        elif l.endswith("map:"):
            map_name = l.split()[0]
            mappings[map_name] = []
        else:
            mappings[map_name] += [[int(n) for n in re.findall(r"\d+", l)]]
    return seeds, mappings


def get_mapped_minimum(value: int, ranges: Ranges) -> int:
    matches = []
    for rng in ranges:
        dest, src, length = rng
        if src <= value < src + length:
            matches.append(dest + (value - src))
    return value if not matches else min(matches)


def find_mapped_value(mappings: Mappings, seed: int):
    def _loop(acc: list[int], mapping: int, keys: list[str]) -> list[int]:
        if keys == []:
            return acc

        mapped_value = get_mapped_minimum(mapping, mappings[keys[0]])
        return _loop(acc + [mapped_value], mapped_value, keys[1:])

    keys = list(mappings.keys())
    return _loop([], seed, keys)


def main[A, B]() -> tuple[A, B]:
    lines = get_input(Path(__file__).parent / "input01.txt")
    seeds, mappings = parse_input(lines)
    results = {seed: find_mapped_value(mappings, seed)[-1] for seed in seeds}
    return min(results.values()), 0


if __name__ == "__main__":
    sol1, sol2 = main()
    # Solution 1: 24848
    print("Solution 1", sol1)
    # Solution 2: 7258152
    print("Solution 2", sol2)
