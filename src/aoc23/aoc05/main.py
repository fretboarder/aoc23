import re
from dataclasses import dataclass, field
from functools import reduce
from itertools import batched
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


@dataclass
class Mapping:
    dst: int
    src: int
    cnt: int


SortedMapping = dict[str, tuple[Mapping, ...]]


@dataclass
class Mapper:
    name: str
    mappings: tuple[Mapping, ...]
    mapping_ranges: tuple[tuple[int, range], ...] = field(init=False)

    def __post_init__(self):
        self.mapping_ranges = tuple(
            [(m.dst - m.src, range(m.src, m.src + m.cnt)) for m in self.mappings]
        )


def parse_input(lines: list[str]) -> tuple[Seeds, Mappings, SortedMapping]:
    mappings = dict()
    seeds = [int(n) for n in re.findall(r"\d+", lines[0])]
    map_name = ""
    for line in lines[1:]:
        if not line:
            continue
        elif line.endswith("map:"):
            map_name = line.split()[0]
            mappings[map_name] = []
        else:
            mappings[map_name] += [[int(n) for n in re.findall(r"\d+", line)]]

    sortedmappings = {k: sorted(v, key=lambda v: v[1]) for k, v in mappings.items()}
    sortedmappings = {
        k: tuple([Mapping(*m) for m in v]) for k, v in sortedmappings.items()
    }
    return seeds, mappings, sortedmappings


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


###############################################################################
# part 2
###############################################################################
SplitRange = tuple[range, ...]
SplitRanges = tuple[range | None, SplitRange]


def is_subrange(mapping: range, seed: range) -> bool:
    # mapping: mmmmmmmmmmmm
    #    seed:   ssssssss
    return (
        mapping.start <= seed.start <= mapping.stop
        and mapping.start <= seed.stop <= mapping.stop
    )


def is_superrange(mapping: range, seed: range) -> bool:
    # mapping :     mmmmmmm
    #    seed : sssssssssssssss
    return seed.start < mapping.start and seed.stop > mapping.stop


def overlap_start(mapping: range, seed: range) -> bool:
    # mapping :     mmmmmmm
    #    seed : sssssss
    return seed.start < mapping.start and mapping.start <= seed.stop <= mapping.stop


def overlap_end(mapping: range, seed: range) -> bool:
    # mapping : mmmmmmm
    #    seed :    sssssss
    return mapping.start <= seed.start <= mapping.stop and seed.stop > mapping.stop


def split_range(seed: range, mapping: range) -> tuple[range]:
    if is_subrange(mapping, seed):
        mapped, unmapped = (seed, ())
    elif is_superrange(mapping, seed):
        mapped, unmapped = (
            mapping,
            (range(seed.start, mapping.start), range(mapping.stop, seed.stop)),
        )
    elif overlap_start(mapping, seed):
        mapped, unmapped = (
            range(mapping.start, seed.stop),
            (range(seed.start, mapping.start),),
        )
    elif overlap_end(mapping, seed):
        mapped, unmapped = (
            range(seed.start, mapping.stop),
            (range(mapping.stop, seed.stop),),
        )
    else:
        mapped, unmapped = None, (seed,)

    return (
        mapped,
        tuple(
            [r for r in unmapped if len(unmapped)],
        ),
    )


@dataclass(frozen=True)
class TheMappings:
    mapped: list[range]
    unmapped: list[range]


def concat_range(r1: range, r2: range) -> range:
    if r1.stop == r2.start or r1.start == r2.stop:
        if r1.start <= r2.start:
            return range(r1.start, r2.stop)
        return range(r2.start, r1.stop)
    elif r2.start <= r1.start <= r2.stop and r2.start <= r1.stop <= r2.stop:
        return r2
    elif r1.start <= r2.start <= r1.stop and r1.start <= r2.stop <= r1.stop:
        return r1
    raise ValueError(
        f"non-continuous ranges {r1} {r2}",
    )


def concat_ranges(*ranges: range) -> range:
    if not ranges:
        raise ValueError("no ranges to concat")
    elif len(ranges) == 1:
        return ranges[0]
    # Use functools.reduce to repeatedly apply concat_range
    return reduce(concat_range, ranges)


def is_continuous(*ranges: range) -> bool:
    try:
        concat_ranges(*ranges)
    except ValueError:
        return False
    else:
        return True


def remove_range(seed: range, sub: range) -> tuple[range]:
    _, remaining = split_range(seed, sub)
    return remaining


def remove_ranges(src: range, *ranges: range) -> tuple[range]:
    if not len(ranges):
        return src
    remainders = []
    for r in sorted(ranges, key=lambda r: r.start):
        res = remove_range(src, r)
        if len(res) < 2:
            return res
        fst, lst = res
        remainders.append(fst)
        src = lst
    return tuple(remainders + [lst])


def collect_mappings(mapper: Mapper, seed: range) -> tuple[list[range], list[range]]:
    def accumulate(
        ranges: TheMappings, mapping_ranges: list[tuple[int, range]]
    ) -> TheMappings:
        if mapping_ranges == []:
            return ranges
        mapped, _ = split_range(seed, mapping_ranges[0][1])
        new_ranges = set([*ranges.mapped, mapped]) if mapped else ranges.mapped
        return accumulate(TheMappings(list(new_ranges), []), mapping_ranges[1:])

    mapped_ranges = accumulate(TheMappings([], []), list(mapper.mapping_ranges))
    # now I have everything that is mappable on that stage
    # to get the remaining range(s) which are unmappable I subtract the mapped
    # ranges from the seed
    if not mapped_ranges.mapped:
        return [], [seed]
    elif (
        len(mapped_ranges.mapped) == 1
        and mapped_ranges.mapped[0] == seed
        or (
            len(mapped_ranges.mapped) > 1
            and is_continuous(*mapped_ranges.mapped)
            and concat_ranges(*mapped_ranges.mapped) == seed
        )
    ):
        return mapped_ranges.mapped, []
    else:
        return mapped_ranges.mapped, list(remove_ranges(seed, *mapped_ranges.mapped))


def get_mapped_range(mapper: Mapper, seed_range: range) -> range:
    for offset, mapped in mapper.mapping_ranges:
        if (
            mapped.start <= seed_range.start <= mapped.stop
            and mapped.start <= seed_range.stop <= mapped.stop
        ):
            return range(seed_range.start + offset, seed_range.stop + offset)
    return seed_range


def push_range_to_stage(mapper: Mapper, seed_range: range) -> list[range]:
    new_mapped, new_unmapped = collect_mappings(mapper, seed_range)
    return [get_mapped_range(mapper, r) for r in new_mapped] + new_unmapped


def find_location(sortedmappings: SortedMapping, seed_ranges: list[range]):
    mappers = [Mapper(name, mappings) for name, mappings in sortedmappings.items()]

    collected: list[range] = []
    for seed_range in seed_ranges:
        stage_results = [seed_range]
        for mapper in mappers:
            stage_results = [push_range_to_stage(mapper, r) for r in stage_results]
            stage_results = list(set([r for sub in stage_results for r in sub]))
        collected += stage_results
    return min([r.start for r in collected])


def main() -> tuple[int, int]:
    lines = get_input(Path(__file__).parent / "input01.txt")
    seeds, mappings, sortedmappings = parse_input(lines)
    solution1 = {seed: find_mapped_value(mappings, seed)[-1] for seed in seeds}

    ranges = [range(seed, seed + length) for seed, length in batched(seeds, 2)]
    solution2 = find_location(sortedmappings, ranges)
    return min(solution1.values()), solution2


if __name__ == "__main__":
    sol1, sol2 = main()
    # Solution 1: 340994526
    print("Solution 1", sol1)
    # Solution 2: 52210644
    print("Solution 2", sol2)
