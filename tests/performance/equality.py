from collections.abc import Mapping
from typing import Any, IO

from tests.performance.helper import *


class FrozendictBase1:
    __slots__ = '__source',

    def __new__(cls, iterable = (), /, **kwargs):
        self = object.__new__(cls)
        self.__source = dict(iterable, **kwargs)
        return self

    def __eq__(self, other: Any, /) -> bool:
        if isinstance(other, FrozendictBase1):
            return self.__source == other.__source

        if isinstance(other, Mapping):
            return other == self.__source

        return NotImplemented


class FrozendictBase2:
    __slots__ = '__source',

    def __new__(cls, iterable = (), /, **kwargs):
        self = object.__new__(cls)
        self.__source = dict(iterable, **kwargs)
        return self

    def __eq__(self, other: Any, /) -> bool:
        return other == self.__source


class FrozendictBase3:
    __slots__ = '__source',

    def __new__(cls, iterable = (), /, **kwargs):
        self = object.__new__(cls)
        self.__source = dict(iterable, **kwargs)
        return self

    def __eq__(self, other: Any, /) -> bool:
        return self.__source == other


implementations = FrozendictBase1, FrozendictBase2, FrozendictBase3

comparisons = [
    ("frozendict == 1", lambda fd, _: dict(v1=fd, v2=1)),
    ("frozendict == 'value'", lambda fd, _: dict(v1=fd, v2='value')),
    ("frozendict == dict", lambda fd, d: dict(v1=fd, v2=d)),
    ("frozendict == frozendict", lambda fd, _: dict(v1=fd, v2=fd)),
    ("frozendict == other_frozendict", lambda fd, d: dict(v1=fd, v2=fd.__class__(d))),
    ]


def run_for_n_values(n: int, io: IO, /):
    d = {f'{i}': i for i in range(1, n + 1)}
    d_shifted = {f'{i}': i + 1 for i in range(1, n + 1)}
    instances = [cls(d) for cls in implementations]

    io.write(f'# {n:,} items in dictionaries\n\n')

    for descr, globals_func in comparisons:
        io.write(f'## {descr}\n\n')

        table = Table(
            ['Implementation', 'Time required, s'],
            [Alignment.LEFT, Alignment.RIGHT],
            io,
            )

        for ins in instances:
            value = get_time_value(
                repeat('v1 == v2', repeat=100, globals=globals_func(ins, d_shifted))
                )
            table.append([f'`{ins.__class__.__name__}`', value.seconds])

        io.write('\n')


with open('reports/equality.md', 'w') as f:
    f.write(report_header())
    for N in [10, 100, 1000]:
        run_for_n_values(N, f)
