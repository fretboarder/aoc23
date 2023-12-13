from pathlib import Path
from pprint import pp
from typing import NamedTuple

import pandas as pd
from aoc23.support import get_input

Grid = list[str]


class Refl(NamedTuple):
    left: int
    right: int


class P1Result(NamedTuple):
    puzzle_id: int
    refl_cols: list[tuple[Refl, int]]
    refl_rows: list[tuple[Refl, int]]
    result: int


def parse_input(mirror_map: list[str]) -> list[Grid]:
    grids = []
    m = []
    for line in mirror_map:
        if line.strip():
            m.append(line)
        else:
            grids.append(pd.DataFrame([list(row) for row in m]))
            m = []
    # append the final map
    grids.append(pd.DataFrame([list(row) for row in m]))
    return grids


def mirrored(grid: pd.DataFrame, middle: Refl) -> int:
    _, cols = grid.shape
    start_left, start_right = middle
    mirrored = 1
    for left, right in zip(range(start_left - 1, -1, -1), range(start_right + 1, cols)):
        if (grid[left] == grid[right]).all():
            mirrored += 1
    return mirrored


def locate_reflection_line(grid: pd.DataFrame) -> list[tuple[Refl, int]]:
    mirror_cols: list[Refl] = []
    for i, _ in grid.items():
        if i > 0 and (grid[i] == grid[i - 1]).all():
            mirror_cols.append(Refl(i - 1, i))

    return [(middle, mirrored(grid, middle)) for middle in mirror_cols]


def is_perfect(grid: pd.DataFrame, middle: Refl, width: int):
    _, cols = grid.shape
    right_edge = middle.right + width - 1
    left_edge = middle.left - width + 1
    if right_edge >= cols - 1 or left_edge <= 0:
        return True

    return False


def solution(puzzle_id: int, g: pd.DataFrame) -> P1Result:
    # loop over columns
    gt = g.transpose()
    mirror_cols = locate_reflection_line(g)
    mirror_rows = locate_reflection_line(gt)
    final_cols = [
        (middle, width) for middle, width in mirror_cols if is_perfect(g, middle, width)
    ]
    final_rows = [
        (middle, width)
        for middle, width in mirror_rows
        if is_perfect(gt, middle, width)
    ]

    if len(final_cols) or len(final_rows):
        assert (
            len(final_cols) == 1
            and len(final_rows) == 0
            or len(final_cols) == 0
            and len(final_rows) == 1
        )
        if final_cols:
            middle, _ = final_cols[0]
            res = middle.left + 1
        else:
            middle, _ = final_rows[0]
            res = 100 * (middle.left + 1)

        return P1Result(puzzle_id, final_cols, final_rows, res)

    # this should never happen
    msg = "Must not end up here"
    raise ValueError(msg)


def solution2(g: pd.DataFrame, p1r: P1Result):
    rows, cols = g.shape

    p1col_refl = set(p1r.refl_cols)
    p1row_refl = set(p1r.refl_rows)

    FINAL_COLS, FINAL_ROWS = [], []
    new_refl_found = False
    for row in range(rows):
        if new_refl_found:
            break
        for col in range(cols):
            orig_sym = g.at[row, col]
            g.at[row, col] = "." if orig_sym == "#" else "."
            gt = g.transpose()

            mirror_cols = [
                refl for refl in locate_reflection_line(g) if refl not in p1col_refl
            ]
            mirror_rows = [
                refl for refl in locate_reflection_line(gt) if refl not in p1row_refl
            ]
            final_cols = [
                (middle, width)
                for middle, width in mirror_cols
                if is_perfect(g, middle, width)
            ]
            final_rows = [
                (middle, width)
                for middle, width in mirror_rows
                if is_perfect(gt, middle, width)
            ]

            if len(final_cols) or len(final_rows):
                pp(f"MATCH when changing {row} / {col} to {g.at[row, col]!r}")
                pp(f"{final_cols=} .. {final_rows=}")
                FINAL_COLS, FINAL_ROWS = final_cols, final_rows
                g.at[row, col] = orig_sym
                new_refl_found = True
                break
            g.at[row, col] = orig_sym

    if FINAL_COLS:
        middle, _ = FINAL_COLS[0]
        res = middle.left + 1
    else:
        middle, _ = FINAL_ROWS[0]
        res = 100 * (middle.left + 1)

    return res


def main() -> tuple[int, int]:
    s0 = [
        solution(i, g)
        for i, g in enumerate(
            parse_input(get_input(Path(__file__).parent / "input01.txt"))
        )
    ]
    s2 = [
        solution2(g, s0[i])
        for i, g in enumerate(
            parse_input(get_input(Path(__file__).parent / "input01.txt"))
        )
    ]

    return sum(p1r.result for p1r in s0), sum(s2)  # solution(galaxies2)


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")
