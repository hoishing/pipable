# Pipable

[![ci-badge]][ci-url] [![pypi-badge]][pypi-url] [![MIT-badge]][MIT-url] [![black-badge]][black-url]

> pipe operation in python

---

> [!NOTE]
> This repository has been archived. While being able to chain function calls with a pipe operator looks handy and more "functional", the trade-off of breaking normal Python coding style outweighed the benefits of the syntactic sugar, especially when working with LLMs. Keeping to the conventional way of writing code is friendlier to LLMs and human readers, and thus enhances productivity.

## Quick Start

### Create the Pipe Object

- instantiate with the `Pipe` class

```python
from pipable import Pipe

list = Pipe(list)
"abc" | list    # ["a", "b", "c"]
```

#### Pipe Object is Partial with Infix Operator

- at the core Pipe create partial function while overriding it's `|` operator
- instantiate Pipe object like the built-in `functools.partial`
- preceding output will be assigned to the **last positional** argument of the Pipe object

```python
square = Pipe(pow, exp=2)
3 | square    # 9
```

Since that Pipe appends preceding output to the last positional argument,
assigning 1st argument with keyword will raise exception.
This behave the same as `functools.partial`

```python
base2 = Pipe(pow, 2)  # positional arg ok
3 | base2    # 8

base2 = Pipe(pow, base=2)  # keyword arg don't
3 | base2    # raise!!
```

### Using Decorator

- `@Pipe` decorator transforms function into Pipe object
- preceding output will be assigned to the last positional argument
- instantiate Pipe decorated function similar to creating partial

```python
# only one argument
@Pipe
def hi(name: str) -> str:
  return f"hi {name}"

"May" | hi    # "hi May"


# multiple arguments
@Pipe
def power(base: int, exp: int) -> int:
  return base ** exp

# instantiate Pipe obj by partially calling the function
2 | power(3)        # 9, note we need to use positional argument here
2 | power(exp=3)    # 8, subsequent arguments can use keyword

# assign the 1st argument with keyword will raise exception
2 | power(base=3)    # raise !!
```

### Passing Variable Length Arguments

- use `>>` operator to pass-in variable length arguments

```python
@Pipe
def kebab(*args):
    return "-".join(args)

["a", "b"] >> kebab   # "a-b"
```

- use `<<` operator to pass variable length keyword arguments

```python
@Pipe
def concat(**kwargs):
    return ", ".join([f"{k}-{v}" for k, v in kwargs.items()])

dict(b="boy", c="cat") << concat    # "b-boy, c-cat"
```

- refer the [docs](https://hoishing.github.io/pipable/reference) for details

## Motivation

Pipe operation is a handy feature in functional programming. It allows us to:

- write more succinct and readable code
- create less variables
- easily create new function by chaining other functions

However it's still a missing feature in Python as of 2023. This package try to mimic pipe operation by overriding the bitwise-or operator, and turn any function into pipable partial.

There are packages, such as [pipe] take the similar approach. It works great with iterables, and create pipe as iterator, ie. open pipe). However, I simply want to take preceding expression as an input argument of the current function then execute it, ie. close pipe. It leads to the creation of this package.

## FAQ

How can I assign value to the first argument?
  
use a wrapper function

```python
square = Pipe(lambda x: pow(x, 2))
3 | square  # 9
```

---

Can I create open pipe?

`Pipe` only create closed pipe, ie. execute the function after piping with the `|` operator. You may consider other solutions such as:

- [pipe], which create open pipe for iterators
- [Coconut], a python variant that embrace functional programming

---

Can I append the preceding output at the beginning of the argument list?

Put the preceding output as the 1st argument of a wrapper function

```python
# prepend is the default behaviour
def kebab(*args):
  return "-".join(*args)

'a' | Pipe(kebab, 'b', 'c')  # 'b c a'

@Pipe
def wrapper(first, others):
  return kebab(first, *others)

'a' | wrapper(others=['b', 'c'])  # 'a b c'
```

## Need Help?

[![git-logo] github issue][github issue]

[![x-logo] posts][x-post]

[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
[ci-badge]: https://github.com/hoishing/pipable/actions/workflows/ci.yml/badge.svg
[ci-url]: https://github.com/hoishing/pipable/actions/workflows/ci.yml
[Coconut]: https://github.com/evhub/coconut
[git-logo]: https://api.iconify.design/bi/github.svg?color=%236FD886&width=20
[github issue]: https://github.com/hoishing/pipable/issues
[MIT-badge]: https://img.shields.io/github/license/hoishing/pipable
[MIT-url]: https://opensource.org/licenses/MIT
[pipe]: https://pypi.org/project/pipe
[pypi-badge]: https://img.shields.io/pypi/v/pipable
[pypi-url]: https://pypi.org/project/pipable/
[x-logo]: https://api.iconify.design/ri:twitter-x-fill.svg?width=20&color=DarkGray
[x-post]: https://x.com/hoishing
