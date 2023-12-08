import pytest
from aoc23 import _version
from aoc23.cli import main
from click.testing import CliRunner


@pytest.fixture()
def client() -> CliRunner:
    return CliRunner()


def test_version(client: CliRunner):
    result = client.invoke(main.cli, "version")
    assert result.exit_code == 0
    assert result.output == f"{_version()}\n"
