from collections.abc import ItemsView, Iterable, Iterator, KeysView, Mapping, ValuesView
from copy import deepcopy
from itertools import chain
from sys import getsizeof
from typing import Generic, Optional, TypeVar, Union, overload, Protocol

K = TypeVar('K')
K_co = TypeVar('K_co', covariant=True)
V_co = TypeVar('V_co', covariant=True)
T = TypeVar('T')
S = TypeVar('S')


class SupportsKeysAndGetItem(Protocol[K, V_co]):
    def keys(self, /) -> Iterable[K]: ...
    def __getitem__(self, item: K, /) -> V_co: ...


@Mapping.register
class frozendict(Generic[K_co, V_co]):
    __slots__ = '_source', '_hash'

    @overload
    def __init__(self, /, **kwargs: V_co): ...
    @overload
    def __init__(self, mapping: SupportsKeysAndGetItem[K_co, V_co], /): ...
    @overload
    def __init__(self, mapping: SupportsKeysAndGetItem[str, V_co], /, **kwargs: V_co): ...
    @overload
    def __init__(self, iterable: Iterable[tuple[K_co, V_co]], /): ...
    @overload
    def __init__(self, iterable: Iterable[tuple[str, V_co]], /, **kwargs: V_co): ...

    def __init__(self, iterable=(), /, **kwargs):
        self._source = dict(iterable, **kwargs)
        self._hash = None

    def __getitem__(self, item: K_co, /) -> V_co:
        return self._source[item]

    @overload
    def get(self, key: K_co, /) -> Optional[V_co]: ...
    @overload
    def get(self, key: K_co, default: V_co, /) -> V_co: ...
    @overload
    def get(self, key: K_co, default: T, /) -> Union[V_co, T]: ...

    def get(self, key, default=None, /):
        return self._source.get(key, default)

    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[T], /) -> 'frozendict[T, None]': ...
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[T], value: S, /) -> 'frozendict[T, S]': ...

    @classmethod
    def fromkeys(cls, iterable: Iterable, value=None, /):
        return cls((k, value) for k in iterable)

    def keys(self, /) -> KeysView[K_co]:
        return self._source.keys()

    def values(self, /) -> ValuesView[V_co]:
        return self._source.values()

    def items(self, /) -> ItemsView[K_co, V_co]:
        return self._source.items()

    # def copy(self, /):
    #     return self

    def __copy__(self, /):
        return self

    def __deepcopy__(self, memo, /):
        if isinstance(self._hash, int):
            return self

        return self.__class__(deepcopy(self._source, memo))

    def __repr__(self, /):
        return f'{self.__class__.__name__}({self._source})'

    def __str__(self, /):
        return str(self._source)

    def __len__(self, /):
        return len(self._source)

    def __contains__(self, item, /):
        return item in self._source

    def __iter__(self, /) -> Iterator[K_co]:
        return iter(self._source)

    def __reversed__(self, /) -> Iterator[K_co]:
        return reversed(self._source)

    def __or__(self, other: Mapping[K_co, V_co], /) -> 'frozendict[K_co, V_co]':
        if isinstance(other, Mapping):
            return self.__class__(chain(self._source.items(), other.items()))

        return NotImplemented

    def __ror__(self, other: Mapping[K_co, V_co], /) -> 'frozendict[K_co, V_co]':
        if isinstance(other, Mapping):
            return self.__class__(chain(other.items(), self._source.items()))

        return NotImplemented

    def __eq__(self, other, /):
        return self._source == other

    def __ne__(self, other, /):
        return self._source != other

    def __hash__(self, /):
        if self._hash is None:
            try:
                self._hash = hash(frozenset(self._source.items()))
            except TypeError as e:
                self._hash = str(e)[18:-1]

        if isinstance(self._hash, int):
            return self._hash

        raise TypeError(f'unhashable type: {self._hash!r}')

    def __getstate__(self, /):
        return self._source

    def __setstate__(self, state, /):
        self._source = state
        self._hash = None

    def __sizeof__(self):
        return object.__sizeof__(self) + getsizeof(self._source) + getsizeof(self._hash)


__all__ = 'frozendict',
