from typing import Callable, Any


def prepend_partial(func: Callable, /, *args, **keywords) -> Callable:
    """partial with arguments prepend to `args`

    Notes:
        built-in `functools.parital` append arguments to `args`, see [docs][py-docs]

    Examples:
        - compare with `functools.partial` using `pow`
        >>> import functools
        >>> square_of = prepend_partial(pow, 2)
        >>> two_power_of = functools.partial(pow, 2)
        >>> square_of(3), two_power_of(3)
        (9, 8)

    Args:
        func (Callalbe): function to create partial, positional only
        args (list): positional arguments of `func`
        keywords (dict): keyword arguments of `func`

    Returns:
        Callable: partial of `func`

    [py-docs]: https://docs.python.org/3/library/functools.html#functools.partial
    """

    def f(*fargs, **fkeywords):
        combined_kwargs = {**keywords, **fkeywords}
        # fargs precede args
        return func(*fargs, *args, **combined_kwargs)

    # competible w/ functools.partial signature
    f.func = func
    f.args = args
    f.keywords = keywords
    return f


class Pipe(object):
    """create pipable function

    Turn the bitwise-or operator `|` into an infix function that accept the output of previous expression.
    ie. pipe operator

    Examples:
        see [README.md#quick-start]
    """

    def __init__(self, func: Callable, *args, **kwargs) -> None:
        """create pipable partial for the target func

        Args:
            func (Callable): func to be pipable
            args: partial's positional args
            kwargs: partial's keyword args
        """
        self.pipe = prepend_partial(func, *args, **kwargs)

    def __ror__(self, precedent: Any):
        """override the builit-in `|` operator, turn it into pipe"""
        # return partial(self.func, precedent)
        return self.pipe(precedent)

    def __call__(self, *args, **kwargs):
        """replace arguments of the pipable partial"""
        return Pipe(self.pipe.func, *args, **kwargs)
