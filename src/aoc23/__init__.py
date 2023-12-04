"""Package initializer module."""
from importlib.metadata import version


def _version() -> str:
    return version("aoc23")
