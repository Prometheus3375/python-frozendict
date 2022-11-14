"""
Set._hash and frozenset.__hash__ have different implementation
since 3.6.5 till 3.9.6 due to https://bugs.python.org/issue26163
Issue description: https://bugs.python.org/issue44704
Issue is fixed in 3.9.7+.
Changelogs:
https://docs.python.org/release/3.10.0/whatsnew/changelog.html#python-3-10-0-release-candidate-1
https://docs.python.org/release/3.9.7/whatsnew/changelog.html#python-3-9-7-final
"""

from collections.abc import Mapping, Set
from typing import IO

from tests.performance.helper import *

# noinspection PyUnresolvedReferences,PyProtectedMember
hsh = Set._hash


def mapping_hash_0(m: Mapping, /) -> int:
    """Calculate hash value of a mapping. All mappings must use this function."""
    return hash(frozenset(m.items()))


def mapping_hash_1(m: Mapping, /) -> int:
    """Calculate hash value of a mapping. All mappings must use this function."""
    # noinspection PyUnresolvedReferences,PyProtectedMember
    return Set._hash(m.items())


def mapping_hash_2(m: Mapping, /) -> int:
    """Calculate hash value of a mapping. All mappings must use this function."""
    return hsh(m.items())


def run_for_n_values(n: int, io: IO, /):
    d = {f'{i}': i for i in range(1, n + 1)}
    _ = d.items()  # if some caching exists
    io.write(f'# {n:,} items in dict\n\n')
    table = Table(
        ['Calculation way', 'Time required, s'],
        [Alignment.LEFT, Alignment.RIGHT],
        io,
        )

    hash_frozenset = get_time_value(repeat('f(d)', globals=dict(d=d, f=mapping_hash_0)))
    table.append(['`hash(frozenset(...))`', hash_frozenset.seconds])

    set_hash = get_time_value(repeat('f(d)', globals=dict(d=d, f=mapping_hash_1)))
    table.append(['`Set._hash(...)`', set_hash.seconds])

    cached_set_hash = get_time_value(repeat('f(d)', globals=dict(d=d, f=mapping_hash_2)))
    table.append(['Cached `Set._hash(...)`', cached_set_hash.seconds])

    io.write('\n')


with open('reports/mapping-hash.md', 'w') as f:
    f.write(report_header())
    for N in [10, 100, 1000, 10_000]:
        run_for_n_values(N, f)
