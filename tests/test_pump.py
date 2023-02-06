from click.testing import CliRunner
from pump import main, upgrade_version
from pytest import mark


def test_main():
    runner = CliRunner()
    result = runner.invoke(main, ["patch"])
    assert result.exit_code == 0


@mark.parametrize(
    "input, output",
    [
        ("major", "1.0.0"),
        ("minor", "0.2.0"),
        ("patch", "0.1.2"),
    ],
)
def test_upgrade_version(input, output):
    assert upgrade_version(input, "0.1.1") == output
