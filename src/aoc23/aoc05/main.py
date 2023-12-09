import re
from dataclasses import dataclass, field
from itertools import batched
from pathlib import Path
from pprint import pp

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
    mappings: Mappings = {}
    seeds = [int(n) for n in re.findall(r"\d+", lines[0])]
    map_name = ""
    for line in lines[1:]:
        if not line:
            continue
        if line.endswith("map:"):
            map_name = line.split()[0]
            mappings[map_name] = []
        else:
            mappings[map_name] += [[int(n) for n in re.findall(r"\d+", line)]]
    return seeds, mappings


def get_mapped_minimum(value: int, ranges: Ranges) -> int:
    matches = []
    for rng in ranges:
        dest, src, length = rng
        if src <= value < src + length:
            matches.append(dest + (value - src))
    return value if not matches else min(matches)


def find_mapped_value(mappings: Mappings, seed: int) -> list[int]:
    def _loop(acc: list[int], mapping: int, keys: list[str]) -> list[int]:
        if keys == []:
            return acc

        mapped_value = get_mapped_minimum(mapping, mappings[keys[0]])
        return _loop([*acc, mapped_value], mapped_value, keys[1:])

    keys = list(mappings.keys())
    return _loop([], seed, keys)


###############################################################################
# part 2
###############################################################################
@dataclass
class Mapping:
    dst: int
    src: int
    cnt: int


@dataclass
class MappingChannel:
    offset: int
    range: range  # noqa: A003


@dataclass
class Mapper:
    name: str
    mappings: tuple[Mapping, ...]
    channels: list[MappingChannel] = field(init=False)

    def __post_init__(self) -> None:
        channels = [
            MappingChannel(m.dst - m.src, range(m.src, m.src + m.cnt))
            for m in self.mappings
        ]
        self.channels = sorted(channels, key=lambda c: c.range.start)

    def process(self, input_range: range) -> list[range]:
        collected_mappings: list[range] = []
        remaining_input = input_range
        for channel in self.channels:
            if (
                remaining_input.start < channel.range.start
                and remaining_input.stop < channel.range.start
            ):  # input range is less than the mapping channel
                collected_mappings.append(remaining_input)  # unmapped, we are done
                break
            if (
                channel.range.start <= remaining_input.start <= channel.range.stop
                and channel.range.start <= remaining_input.stop <= channel.range.stop
            ):  # input range is a subrange of the mapping channel
                collected_mappings.append(
                    range(
                        remaining_input.start + channel.offset,
                        remaining_input.stop + channel.offset,
                    )  # mapped range, and done
                )
                break
            if (
                remaining_input.start < channel.range.start
                and channel.range.start <= remaining_input.stop <= channel.range.stop
            ):
                collected_mappings.append(
                    range(remaining_input.start, channel.range.start)
                )  # unmapped up to the start of the channel start
                collected_mappings.append(
                    range(
                        channel.range.start + channel.offset,
                        remaining_input.stop + channel.offset,
                    )  # mapped from channel start to input range stop, and done
                )
                break
            if (
                channel.range.start <= remaining_input.start <= channel.range.stop
                and remaining_input.stop > channel.range.stop
            ):  # input range start within channel range input range stop is larger
                collected_mappings.append(
                    range(
                        remaining_input.start + channel.offset,
                        channel.range.stop + channel.offset,
                    )  # mapped input range start to channel range stop
                )
                # now we have a remaining portion of the input range
                remaining_input = range(channel.range.stop, remaining_input.stop)
            if (
                remaining_input.start < channel.range.start
                and remaining_input.stop > channel.range.stop
            ):  # channel range is a sub range of the input range
                collected_mappings.append(
                    range(remaining_input.start, channel.range.start)
                )  # unmapped up to the start of the channel start
                collected_mappings.append(
                    range(
                        channel.range.start + channel.offset,
                        channel.range.stop + channel.offset,
                    )  # mapped input range start to channel range stop
                )
                # now we have a remaining portion of the input range
                remaining_input = range(channel.range.stop, remaining_input.stop)

            # otherwise the entire input was larger than the channel range
            # continue with the next channel

        # if collected mappings are empty then the input range hasn't been mapped
        # by any channel, so return it unmapped
        return [m for m in collected_mappings if m.start != m.stop] or [remaining_input]


def find_location(mappings: Mappings, seed_ranges: list[range]) -> int:
    mappers = [
        Mapper(name, tuple([Mapping(*m) for m in mps]))
        for name, mps in mappings.items()
    ]
    for m in mappers:
        stage_results = [m.process(seed_range) for seed_range in seed_ranges]
        # flatten list resulting from feeding all seed ranges into a single stage
        seed_ranges = [rng for result in stage_results for rng in result]
    return min([r.start for r in seed_ranges])


def main() -> tuple[int, int]:
    lines: list[str] = get_input(Path(__file__).parent / "input01.txt")
    seeds, mappings = parse_input(lines)
    solution1 = {seed: find_mapped_value(mappings, seed)[-1] for seed in seeds}
    ranges = [range(seed, seed + length) for seed, length in batched(seeds, 2)]
    return min(solution1.values()), find_location(mappings, ranges)


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1 {sol1}")
    pp(f"Solution 2 {sol2}")
