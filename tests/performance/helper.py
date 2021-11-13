import platform
from datetime import datetime
from enum import Enum
from typing import NamedTuple, IO


class TimeValue(NamedTuple):
    value: float
    formatted: str

    def __str__(self, /): return self.formatted


def get_time_value(values: list[float], /) -> TimeValue:
    v = min(values)
    return TimeValue(v, f'{v:.9f}')


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
