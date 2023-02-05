from click.testing import CliRunner
from pump import main


def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(main, ["patch"])
    assert result.exit_code == 0
