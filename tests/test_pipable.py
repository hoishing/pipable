from pipable import Pipe
import pytest


# ===== fixture ======
@Pipe
def pow_pipe(base: int, exp: int) -> int:
    """func to test decorator"""
    return base**exp


# ====== tests ========
def test_builtn_with_single_arg():
    list_ = Pipe(list)
    assert "ab" | list_ == ["a", "b"]


def test_builtin_with_multiple_args():
    square = Pipe(pow, exp=2)
    assert 3 | square == 9


def test_raise_by_assigning_1st_arg():
    base2 = Pipe(pow, base=2)
    with pytest.raises(Exception):
        3 | base2


def test_decorator_with_single_arg():
    @Pipe
    def hi(name):
        return f"hi {name}"

    assert "May" | hi == "hi May"


def test_decorated_with_multiple_args():
    assert 3 | pow_pipe(exp=2) == 9


def test_decorator_raise_assigning_first_arg():
    with pytest.raises(Exception):
        3 | pow_pipe(base=2)


def test_wrap_with_partial():
    base2 = Pipe(lambda x: pow(2, x))
    assert 3 | base2 == 8


def test_prepend_preceding(capsys):
    prepend = Pipe(print, "b", "c")
    "a" | prepend
    stdout: str = capsys.readouterr().out
    assert stdout.splitlines()[-1] == "a b c"


def test_append_preceding(capsys):

    append = Pipe(lambda x: print(1, 2, x))
    3 | append
    stdout: str = capsys.readouterr().out
    assert stdout.splitlines()[-1] == "1 2 3"
