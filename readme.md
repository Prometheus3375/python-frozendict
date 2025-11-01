`frozendict-x` is a library that provides a typed wrapper around dictionaries to protect them from 
updates and thus gain some other properties like being hashable.

This repo is an archive.
The development is continued [here](https://github.com/Prometheus3375/python-misc).

# Usage

Use frozendict when you need an immutable mapping with the next properties:
- hashable;
- subclass-able;
- supports copy and pickle modules.

# Some facts

Values inside a frozendict may be unhashable like in a tuple.

`copy` and `deepcopy` usually return the same object if it is hashable.
It is true for the tuple, but not true for frozenset (https://bugs.python.org/issue44703).
