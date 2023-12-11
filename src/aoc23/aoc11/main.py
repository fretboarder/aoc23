from pathlib import Path
from pprint import pp
from typing import NamedTuple

import numpy as np
import pandas as pd
from aoc23.support import get_input


class Pos(NamedTuple):
    col: int  # x
    row: int  # y


Grid = list[str]


def update_galaxy_positions(
    galaxies: list[Pos],
    empty_cols: list[str],
    empty_rows: list[int],
    expansion_factor: int,
) -> list[Pos]:
    def pos_less_than(empty: list[int], coord: int) -> int:
        return len([e for e in empty if e < coord])

    new_pos = []
    for g in galaxies:
        new_col = g.col + ((expansion_factor - 1) * pos_less_than(empty_cols, g.col))
        new_row = g.row + ((expansion_factor - 1) * pos_less_than(empty_rows, g.row))
        new_pos.append(Pos(new_col, new_row))
    return new_pos


def parse_input(grid: Grid, expansion_factor: int) -> list[Pos]:
    # Create a DataFrame from the grid
    galaxymap = pd.DataFrame([list(row) for row in grid])

    # find rows which are empty
    empty_rows = galaxymap[
        galaxymap.apply(
            lambda row: all(len(str(val)) == 1 and val == "." for val in row), axis=1
        )
    ]
    # find columns which are empty
    empty_cols = galaxymap.loc[
        :,
        galaxymap.apply(
            lambda col: all(len(str(val)) == 1 and val == "." for val in col)
        ),
    ]
    # galaxy coordinates
    galaxies = np.column_stack(np.where(galaxymap == "#"))
    # Convert coordinates to namedtuples
    galaxy_positions = [Pos(col, row) for row, col in galaxies]

    return update_galaxy_positions(
        galaxy_positions,
        list(empty_cols.columns),
        list(empty_rows.index),
        expansion_factor,
    )


def manhattan(pos1: Pos, pos2: Pos) -> int:
    return int(abs(pos2.col - pos1.col) + abs(pos2.row - pos1.row))


def solution(galaxies: list[Pos]) -> int:
    distances = [
        manhattan(g0, g1) for i, g0 in enumerate(galaxies) for g1 in galaxies[i + 1 :]
    ]
    return sum(distances)


def main() -> tuple[int, int]:
    galaxies1 = parse_input(get_input(Path(__file__).parent / "input01.txt"), 2)
    galaxies2 = parse_input(get_input(Path(__file__).parent / "input01.txt"), 1000000)
    return solution(galaxies1), solution(galaxies2)


if __name__ == "__main__":
    sol1, sol2 = main()
    pp(f"Solution 1: {sol1}")
    pp(f"Solution 2: {sol2}")
