# Advent Of Code 2023


[![pytest](https://github.com/fretboarder/aoc23/actions/workflows/unittest.yml/badge.svg)](https://github.com/fretboarder/aoc23/actions/workflows/unittest.yml)
[![ruff](https://github.com/fretboarder/aoc23/actions/workflows/ruff.yml/badge.svg)](https://github.com/fretboarder/aoc23/actions/workflows/ruff.yml)
[![mypy](https://github.com/fretboarder/aoc23/actions/workflows/mypy.yml/badge.svg)](https://github.com/fretboarder/aoc23/actions/workflows/mypy.yml)
[![Release Creation](https://github.com/fretboarder/aoc23/actions/workflows/releaseplease.yml/badge.svg)](https://github.com/fretboarder/aoc23/actions/workflows/releaseplease.yml)

---

## Preparations

```
$ git clone ...
$ cd aoc23
$ poetry install
```

## Running the CLI

```
$ aoc
Usage: aoc [OPTIONS] COMMAND [ARGS]...

  CLI arguments and options.

Options:
  --help  Show this message and exit.

Commands:
  day        Execute and print solutions for a day.
  solutions  Execute and print solutions for all days available.
  version    Print application version.
```

## Examples

```
$ aoc day 1
Solution 1: ...
Solution 2: ...
```

```
$ aoc solutions
========== DAY 01 ==========
  Solution 1: ...
  Solution 2: ...
========== DAY 02 ==========
  ...
```
