from pipable import Pipe
import pytest


# == fixture ==
@Pipe
def kebab(*args):
    return "-".join(args)


@Pipe
def concat(**kwargs):
    return ", ".join([f"{k}-{v}" for k, v in kwargs.items()])


# == test ==
def test_iterable_precedent():
    assert ["a", "b"] >> kebab == "a-b"


def test_dict_precedent():
    assert dict(b="boy", c="cat") << concat == "b-boy, c-cat"
