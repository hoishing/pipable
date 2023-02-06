from pipable import Pipe
import pytest


# == fixture ==
def kebab(*args):
    return "-".join(args)


# == test ==
def test_builtn_with_single_arg():
    list_ = Pipe(list)
    assert "ab" | list_ == ["a", "b"]


def test_precedent_assign_to_last_pos_args():
    assert "c" | Pipe(kebab) == "c"
    assert "c" | Pipe(kebab, "a") == "a-c"
    assert "c" | Pipe(kebab, "a", "b") == "a-b-c"


def test_assign_1st_arg():
    base2 = Pipe(pow, 2)
    assert 3 | base2 == 8


def test_raise_pos_and_keyword_arg_conflict():
    """
    precedent will append to the positional argument list
    ∴ partial can't assign 1st arg as keyword
    """
    base2 = Pipe(pow, base=2)
    with pytest.raises(Exception):
        3 | base2


def test_decorator_with_single_arg():
    @Pipe
    def hi(name):
        return f"hi {name}"

    assert "May" | hi == "hi May"


def test_decorator_with_multiple_arg():
    @Pipe
    def power(base, exp):
        return base**exp

    assert 3 | power(2) == 8
    assert 3 | power(exp=2) == 9
    # same reason with test_raise_pos_and_keyword_arg_conflict
    with pytest.raises(Exception):
        3 | power(base=2)


def test_wrap_with_partial():
    base2 = Pipe(lambda x: pow(2, x))
    assert 3 | base2 == 8


def test_variable_positional_args(capsys):
    print_ = Pipe(print, "a", "b")
    "c" | print_
    stdout: str = capsys.readouterr().out
    assert stdout.splitlines()[-1] == "a b c"


def test_prepend_args_with_wrapper():
    def wrapper(first, others):
        return kebab(first, *others)

    assert "c" | Pipe(wrapper, others=["a", "b"]) == "c-a-b"


def test_decorator_prepend_args():
    @Pipe
    def wrapper(first, args):
        return kebab(first, *args)

    assert "c" | wrapper(args=["a", "b"]) == "c-a-b"


def test_reassign_with_wrapper():
    def kebab(*args):
        return "-".join(args)

    def wrapper(first, others):
        return kebab(first, *others)

    # works
    assert "a" | Pipe(wrapper, others=["b", "c"]) == "a-b-c"

    # works with other var name
    kebab_ = Pipe(wrapper, others=["b", "c"])
    assert "a" | kebab_ == "a-b-c"

    # not work, ∵ original name already re-assigned when wrapper is being invoked
    # it become a Pipe object instead
    kebab = Pipe(wrapper, others=["b", "c"])
    result = "a" | kebab
    assert result != "a-b-c"
    assert isinstance(result, Pipe)
