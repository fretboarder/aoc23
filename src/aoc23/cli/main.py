"""Tool description."""

from importlib import import_module

import click
from aoc23 import _version
from aoc23.support import sha256


@click.group()
def cli() -> None:
    """CLI arguments and options."""


@cli.command()
def version() -> None:
    """Print application version."""
    click.echo(f"{_version()}")


@cli.command()
@click.argument("day")
def day(day: str) -> None:
    """Execute and print solutions for a day."""
    module_name = f"aoc23.aoc{int(day):02}.main"
    day_module = import_module(module_name)
    sol1, sol2 = day_module.main()
    click.echo(f"Solution 1: {sol1}")
    click.echo(f"Solution 2: {sol2}")


@cli.command()
def solutions() -> None:
    """Execute and print solutions for all days available."""
    for d in range(1, 25):
        module_name = f"aoc23.aoc{d:02}.main"
        try:
            day_module = import_module(module_name)
            sol1, sol2 = day_module.main()
            click.echo(f"========== DAY {d:02} ==========")
            click.echo(f"  Solution 1: {sha256(sol1)}")
            click.echo(f"  Solution 2: {sha256(sol2)}")
        except ModuleNotFoundError:
            pass


def main() -> None:
    """Entry function."""
    try:
        cli()
    except Exception as ex:  # noqa: BLE001
        click.secho(f"{ex}", err=True)


if __name__ == "__main__":
    main()
