# pipable

> pseudo pipe operation in python

[![ci-badge]][ci-url] [![coverage-badge]][coverage-url] [![pypi-badge]][pypi-url] [![py-version]][py-url] [![MIT-badge]][MIT-url] [![black-badge]][black-url]

🔗 [source code](https://github.com/hoishing/pipable)

## Quick Start

### Create the Pipe Object

- instantiate with the `Pipe` class

```python
from pipable import Pipe

list_ = Pipe(list)
"abc" | list_    # ["a", "b", "c"]
```

#### Create Pipe Object Like Partial

- turn function into Pipe by providing argument values like using the built-in `functools.partial`
- preceding output will be assigned to the first argument while piping

```python
square = Pipe(pow, exp=2)
3 | square    # 9
```

Note that assigning value to the first argument will raise exception, as it is preserved for the preceding output.

```python
base2 = Pipe(pow, base=2)
3 | base2    # raise !!
```

### Using Decorator

- transform function to Pipe factory function with the `@Pipe` decorator
- preceding output will be assigned to the first argument
- instantiate Pipe object like creating partial by skipping the first argument

```python
# function with only one argument
@Pipe
def hi(name: str) -> str:
  return f"hi {name}"

"May" | hi    # "hi May"


# function with multiple arguments
@Pipe
def power(base: int, exp: int) -> int:
  return a ** b

# instantiate Pipe obj by calling without the 1st argument
2 | power(3)        # 8
2 | power(exp=3)    # 8, better be more explicit with keyword

# assign the 1st argument will cause exception
2 | power(base=3)    # raise !!
```

## Motivation

Pipe operation is a handy feature in functional programming. It allows us to:

- write clearer and more readable code
- create less variables
- easily create new functionality by chaining the output of other functions

However it's still a missing feature in Python as of 2023. This package try to mimic pipe operation by overriding the bitwise-or operator, turn it into an infix function that take the output of previous expression as the first argument of the current function.

There are packages, such as [Pipe][pipe] take the similar approach. It treats pipe as iterator and work great with iterables. However, I simply want to take preceding expression as an input argument of a function then execute it. It leads to the creation of this package.

## FAQ

How can I assign value to the first argument?
  
Assign it within a wrapper function

```python
base2 = Pipe(lambda x: pow(2, x))
3 | base2  # 8
```

---

Can I create open pipe?

`Pipe` only create closed pipe, ie. execute the function after piping with the `|` operator. You may consider other solutions such as:

- [pipe][pipe], which create open pipe for iterators
- [Coconut][coconut], a python variant that embrace functional programming

---

Can I append the preceding output at the end of the argument list?

Put the preceding output at the end using a wrapper function

```python
# prepend is the default behaviour
prepend = Pipe(print, 'b', 'c')
'a' | prepend    # 'a b c'

# use wrapper if you need append
append = Pipe(lambda x: print(1, 2, x))
3 | append    # '1 2 3'
```

## Need Help?

Open a [github issue](https://github.com/hoishing/pipable/issues) or ping me on [Twitter](https://twitter.com/hoishing) ![](https://api.iconify.design/logos/twitter.svg?width=20)

[ci-badge]: https://github.com/hoishing/pipable/actions/workflows/ci.yml/badge.svg
[ci-url]: https://github.com/hoishing/pipable/actions/workflows/ci.yml
[coverage-badge]: https://hoishing.github.io/pipable/assets/coverage-badge.svg
[coverage-url]: https://hoishing.github.io/pipable/assets/coverage/
[MIT-badge]: https://img.shields.io/github/license/hoishing/pipable
[MIT-url]: https://opensource.org/licenses/MIT
[pypi-badge]: https://img.shields.io/pypi/v/pipable
[pypi-url]: https://pypi.org/project/pipable/
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
[py-version]: https://img.shields.io/pypi/pyversions/pipable
[py-url]: https://python.org
[pipe]: https://pypi.org/project/pipe
[coconut]: https://github.com/evhub/coconut
