# pipable

> pseudo pipe operation in python

[![CI][ci-badge]][ci-url] [![Coverage][coverage-badge]][coverage-url] [![MIT][MIT-badge]][MIT-url]

🔗 [source code](https://github.com/hoishing/pipable)

## Quick Start

### Create Pipe Object

- instantiate with the `Pipe` class

```python
from pipable import Pipe

list_ = Pipe(list)
"abc" | list_  # ["a", "b", "c"]
```

#### Pipe Object is Partial

- provide argument values to create the partial like using built-in `functools.partial`
- preceding output will assign to the first argument while calling

```python
square = Pipe(pow, exp=2)
3 | square  # 9
```

Note that assigning value to the first argument will raise exception, as it is preserved for the preceding output.

```python
base2 = Pipe(pow, base=2)
3 | base2  # raise ⚠️
```

### Using Decorator

- transform function to Pipe obj with the `@Pipe` decorator
- preceding output will be assigned to the first argument
- create Pipe object by calling the function with non-first arguments

```python
# function with only one argument
@Pipe
def hi(name: str) -> str:
  return f"hi {name}"

"May" | hi  # "hi May"


# function with multiple arguments
@Pipe
def power(base: int, exp: int) -> int:
  return a ** b

# assign non-first argument to create Pipe obj
2 | power(3)      # 8, first arg automatically skipped
2 | power(exp=3)  # 8, explicit assign with keyword is better

# assign the 1st argument raise exception
2 | power(base=3)  # raise ⚠️
```

## Motivation

Pipe operation is a handy feature in functional programming. It allows us to:

- write clearer and more readable code
- create less variables
- easily create new functionality by chaining the output of other functions

However it's still a missing feature in Python as of 2023. This package try to mimic pipe operation by overriding the bitwise-or operator, turn it into an infix function that take the output of previous expression as the first argument of the current function.

There are packages, such as [Pipe][pipe] take the similar approach. It treats pipe as iterator and work great with iterables. However, I simply want to take preceding expression as an input argument of a function then execute it. It leads to the creation of this package.

## FAQ

Q: I want to assign value to the first argument
A: use `functools.partial` to wrap your function first

```python
from functools import partial
from pipable import Pipe

base2 = Pipe(partial(pow, base=2))
3 | base2  # 8
```

- Q: I want to create open pipe
- A: `Pipe` only create closed pipe, ie. execute the function when chaining with the `|` operator. You may consider other solutions such as:
  - [pipe][pipe], which create open pipe for iterators since version 2
  - [Coconut][coconut], a python variant that embrace functional programming

## Need Help?

Open a [github issue](https://github.com/hoishing/pipable/issues) or ping me on [Twitter](https://twitter.com/hoishing) ![](https://api.iconify.design/logos/twitter.svg?width=20)

[ci-badge]: https://github.com/hoishing/pipable/actions/workflows/ci.yml/badge.svg
[ci-url]: https://github.com/hoishing/pipable/actions/workflows/ci.yml
[coverage-badge]: https://hoishing.github.io/pipable/assets/coverage-badge.svg
[coverage-url]: https://hoishing.github.io/pipable/assets/coverage/
[MIT-badge]: https://img.shields.io/github/license/hoishing/pipable
[MIT-url]: https://opensource.org/licenses/MIT
[pipe]: https://pypi.org/project/pipe
[coconut]: https://github.com/evhub/coconut
