from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from pprint import pp
from typing import NamedTuple

from aoc23.support import get_input

Steps = tuple[str, ...]


class Lens(NamedTuple):
    label: str
    flen: int


@dataclass(frozen=True)
class Box:
    id: int  # noqa: A003
    lenses: list[Lens]

    def index(self, label: str) -> int:
        for i, lens in enumerate(self.lenses):
            if lens.label == label:
                return i
        return -1


def parse_input(input_lines: list[str]) -> Steps:
    return tuple(input_lines[0].split(","))


def parse_lens(step: str) -> Lens:
    if step.endswith("-"):
        return Lens(step[:-1], -1)
    label, flen = step.split("=")
    return Lens(label, int(flen))


def remove_lens(box: Box, lens: Lens) -> Box:
    return Box(box.id, [_lens for _lens in box.lenses if _lens.label != lens.label])


def update_lens(box: Box, index: int, lens: Lens) -> Box:
    lenses = list(box.lenses)
    lenses[index] = lens
    return Box(box.id, lenses)


def insert_lens(box: Box, lens: Lens) -> Box:
    return (
        update_lens(box, p, lens)
        if (p := box.index(lens.label)) != -1
        else Box(box.id, [*box.lenses, lens])
    )


def boxpower(box: Box) -> int:
    return sum(
        (1 + box.id) * li * lens.flen for li, lens in enumerate(box.lenses, start=1)
    )


def holiday_hash(step: str) -> int:
    return reduce(lambda acc, c: ((acc + ord(c)) * 17) % 256, step, 0)


def update_boxes(boxes: list[Box], lens: Lens) -> list[Box]:
    box_id = holiday_hash(lens.label)
    box, new_boxes = boxes[box_id], [*boxes]
    new_boxes[box_id] = (
        remove_lens(box, lens) if lens.flen == -1 else insert_lens(box, lens)
    )
    return new_boxes


def solution2(lenses: list[Lens]) -> int:
    final_boxes = reduce(update_boxes, lenses, [Box(i, []) for i in range(256)])
    return sum([boxpower(b) for b in final_boxes])


def solution1(steps: Steps) -> int:
    return sum([holiday_hash(step) for step in steps])


def main() -> tuple[int, int]:
    steps = parse_input(get_input(Path(__file__).parent / "input01.txt"))
    return solution1(steps), solution2([parse_lens(step) for step in steps])


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")
