import platform
import sys
from collections.abc import Callable, Iterable
from datetime import datetime
from enum import Enum
from multiprocessing import Process, cpu_count
from time import perf_counter_ns, sleep
from timeit import repeat as timeit_repeat
from typing import Any, IO

import psutil


class TimeValue:
    __slots__ = '__value', '__formatted'

    def __init__(self, value: int, /):
        self.__value = value
        self.__formatted = f'{value:09}'

    def __add_period(self, pos_n: int, /) -> str:
        chars = list(self.__formatted)
        chars.insert(-pos_n, '.')
        if chars[-1] == '.':
            chars.pop()

        result = ''.join(chars).lstrip('0')
        if result[0] == '.':
            result = '0' + result
        return result

    @property
    def value(self, /):
        return self.__value

    @property
    def seconds(self, /):
        return self.__add_period(9)

    @property
    def milli(self, /):
        return self.__add_period(6)

    @property
    def micro(self, /):
        return self.__add_period(3)

    @property
    def nano(self, /):
        return self.__formatted

    def __str__(self, /):
        return self.__formatted

    def __eq__(self, other, /):
        return other == self.__value

    def __lt__(self, other, /):
        return other > self.__value

    def __hash__(self, /):
        return hash(self.__value)


def repeat(
        stmt: str = None,
        setup: str = None,
        repeat: int = None,
        number: int = None,
        globals: dict[str, Any] = None
        ) -> list[int]:
    kw = dict(
        timer=perf_counter_ns,
        stmt=stmt,
        setup=setup,
        repeat=repeat,
        number=number,
        globals=globals
        )
    kw = {k: v for k, v in kw.items() if v is not None}
    # noinspection PyTypeChecker
    return timeit_repeat(**kw)


def get_time_value(values: list[int], /) -> TimeValue:
    return TimeValue(min(values))


def report_header():
    return (
        '# Info\n\n'
        f'- **UTC date**: {datetime.utcnow()}\n'
        f'- **Platform**: {platform.platform(aliased=True)}\n'
        f'- **Python version**: {platform.python_version()}\n'
        f'- **Python compiler**: {platform.python_compiler()}\n'
        f'- **Processor**: {platform.processor()}\n'
        '\n'
    )


class Alignment(Enum):
    NONE = '---'
    LEFT = ':---'
    CENTER = ':---:'
    RIGHT = '---:'


class Table:
    def __init__(self, headers: list[str], /, alignment: list[Alignment] = None, *ios: IO):
        assert len(headers) > 0
        assert all(io.writable() for io in ios)

        if isinstance(alignment, list):
            assert len(headers) == len(alignment)
            alignment = [a.value for a in alignment]
        else:
            alignment = [Alignment.NONE.value for _ in headers]

        self._rows = [headers.copy(), alignment]
        self._header_written = False
        self._ios = ios

    @staticmethod
    def _convert(row: list[str], /) -> str:
        return f'| {" | ".join(row)} |\n'

    def _convert_rows(self, /, start: int = 0) -> str:
        return ''.join(self._convert(self._rows[i]) for i in range(start, len(self._rows)))

    def append(self, row: list, /) -> list[int]:
        row = [str(o) for o in row]
        self._rows.append(row)

        if self._header_written:
            return [io.write(self._convert(row)) for io in self._ios]

        result = [io.write(self._convert_rows()) for io in self._ios]
        self._header_written = True
        return result

    def __str__(self, /):
        return self._convert_rows()


VALUE_SEP = '|'


class Tester(Process):
    def __init__(
            self,
            target: Callable[[...], Iterable],
            raw_result_file: str,
            sleep_time: float = 0,
            /,
            *args,
            **kwargs
            ):
        super().__init__()
        self.__file_path = raw_result_file
        self.__sleep_time = sleep_time
        self.__target = target
        self.__args = args
        self.__kwargs = kwargs

    if sys.platform == 'win32':  # Windows (either 32-bit or 64-bit)
        @staticmethod
        def set_highest_process_priority(pid: int, /):
            psutil.Process(pid).nice(psutil.REALTIME_PRIORITY_CLASS)
    else:  # linux, MAC OS X or other
        @staticmethod
        def set_highest_process_priority(pid: int, /):
            psutil.Process(pid).nice(20)

    def run(self, /):
        self.set_highest_process_priority(self.pid)

        if self.__sleep_time > 0: sleep(self.__sleep_time)

        result = self.__target(*self.__args, **self.__kwargs)
        with open(self.__file_path, 'a') as f:
            f.write(VALUE_SEP.join(map(str, result)))
            f.write('\n')


def run_processes(processes: list[Process], /, sleep_time: float = 1, print_log: bool = True):
    concurrent_n = max(cpu_count() // 2, 1)
    if print_log: print('number of concurrent processes is', concurrent_n)
    processes_to_run = list(reversed(processes))
    running_processes = set()

    while True:
        while len(running_processes) < concurrent_n:
            if not processes_to_run: break
            proc = processes_to_run.pop()
            running_processes.add(proc)
            proc.start()

        sleep(sleep_time)

        for proc in tuple(running_processes):
            if not proc.is_alive():
                running_processes.discard(proc)

        if not (processes_to_run or running_processes): break

    if print_log: print('all processes exited')


def read_raw_result(path: str, /):
    with open(path, 'r') as f:
        data = [line[:-1].split(VALUE_SEP) for line in f]

    return {tuple(parts[:-1]): parts[-1] for parts in data}


__all__ = (
    'TimeValue',
    'repeat',
    'get_time_value',
    'report_header',
    'Alignment',
    'Table',
    'Tester',
    'run_processes',
    'read_raw_result',
    )
