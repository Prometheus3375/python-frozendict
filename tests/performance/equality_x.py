from collections.abc import Mapping
from typing import Any, Callable

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


def cmp_1(fd, _): return dict(v1=fd, v2=1)


def cmp_value(fd, _): return dict(v1=fd, v2='value')


def cmp_dict(fd, d): return dict(v1=fd, v2=d)


def cmp_self(fd, _): return dict(v1=fd, v2=fd)


def cmp_other(fd, d): return dict(v1=fd, v2=fd.__class__(d))


comparisons = [
    ("frozendict == 1", cmp_1),
    ("frozendict == 'value'", cmp_value),
    ("frozendict == dict", cmp_dict),
    ("frozendict == frozendict", cmp_self),
    ("frozendict == other_frozendict", cmp_other),
    ]

descriptions = [cmp[0] for cmp in comparisons]


def run_test(
        n: int,
        cls: type,
        globals_func: Callable[[Any, dict], dict[str, Any]],
        description: str,
        /,
        ):
    d = {f'{i}': i for i in range(1, n + 1)}
    d_shifted = {f'{i}': i + 1 for i in range(1, n + 1)}
    instance = cls(d)

    value = get_time_value(
        repeat(
            'v1 == v2',
            repeat=1000000,
            number=1,
            globals=globals_func(instance, d_shifted),
            )
        )

    return n, description, cls.__name__, value.micro


def run_tests(*sizes: int):
    raw_file_path = 'reports/raw/equality.txt'
    md_file_path = 'reports/equality-x.md'

    # clear raw file
    open(raw_file_path, 'w').close()

    processes = []
    for n in sizes:
        d = {f'{i}': i for i in range(1, n + 1)}
        d_shifted = {f'{i}': i + 1 for i in range(1, n + 1)}
        instances = [cls(d) for cls in implementations]

        for descr, globals_func in comparisons:
            for i, cls in enumerate(implementations):
                _globals = globals_func(instances[i], d_shifted)
                proc = Tester(run_test, raw_file_path, 1 / 8, n, cls, globals_func, descr)
                processes.append(proc)

    run_processes(processes)

    raw = read_raw_result(raw_file_path)
    base_impl = implementations[0]
    other_impls = implementations[1:]

    with open(md_file_path, 'w') as f:
        f.write(report_header())
        for n in sizes:
            f.write(f'# {n:,} items in dictionaries\n\n')

            for descr in descriptions:
                f.write(f'## {descr}\n\n')

                table = Table(
                    ['Implementation', 'Time required, μs'],
                    [Alignment.LEFT, Alignment.RIGHT],
                    f,
                    )

                value = raw[str(n), descr, base_impl.__name__]
                table.append([f'`{base_impl.__name__}`', value])

                for cls in other_impls:
                    value = raw[str(n), descr, cls.__name__]
                    table.append([f'`{cls.__name__}`', value])

                f.write('\n')


if __name__ == '__main__':
    run_tests(10, 100, 1000)
