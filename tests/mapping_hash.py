"""
Set._hash and frozenset.__hash__ have different implementation
since 3.6.5 till 3.9.6 due to https://bugs.python.org/issue26163
Issue description: https://bugs.python.org/issue44704
Issue is fixed in 3.9.7+.
Changelogs:
https://docs.python.org/release/3.10.0/whatsnew/changelog.html#python-3-10-0-release-candidate-1
https://docs.python.org/release/3.9.7/whatsnew/changelog.html#python-3-9-7-final
"""

import platform
from collections.abc import Set, Mapping
from datetime import datetime
from timeit import repeat

# noinspection PyUnresolvedReferences,PyProtectedMember
hsh = Set._hash
d = {i: i for i in range(10)}
items = d.items()


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


def gen_report_text(
    hash_frozenset: list[float],
    set_hash: list[float],
    set_hash_cached: list[float],
    /,
) -> str:
    return (
        '# Info\n\n'
        f'- **UTC date**: {datetime.utcnow()}\n'
        f'- **Platform**: {platform.platform(aliased=True)}\n'
        f'- **Python version**: {platform.python_version()}\n'
        f'- **Python compiler**: {platform.python_compiler()}\n'
        f'- **Processor**: {platform.processor()}\n'
        '\n'
        f'# Details\n\n'
        f'| Calculation way         | Time required, s |\n'
        f'| :---                    |             ---: |\n'
        f'| `hash(frozenset(...))`  |      {min(hash_frozenset):.9f} |\n'
        f'| `Set._hash(...)`        |      {min(set_hash):.9f} |\n'
        f'| Cached `Set._hash(...)` |      {min(set_hash_cached):.9f} |\n'
    )


report = gen_report_text(
    repeat('f(d)', globals=dict(d=d, f=mapping_hash_0)),
    repeat('f(d)', globals=dict(d=d, f=mapping_hash_1)),
    repeat('f(d)', globals=dict(d=d, f=mapping_hash_2)),
)

print(report)

with open('reports/mapping-hash.md', 'w') as f:
    f.write(report)
