from collections.abc import Hashable, ItemsView, Iterable, Iterator, KeysView, Mapping, ValuesView
from copy import deepcopy
from itertools import chain
from sys import getsizeof
from typing import Any, Generic, Optional, Protocol, TypeVar, Union, overload

K = TypeVar('K')
K_co = TypeVar('K_co', covariant=True)
V_co = TypeVar('V_co', covariant=True)
T = TypeVar('T')


class SupportsKeysAndGetItem(Protocol[K, V_co]):
    def keys(self, /) -> Iterable[K]: ...
    def __getitem__(self, item: K, /) -> V_co: ...


def mapping_hash(m: Mapping, /) -> int:
    """Calculate hash value of a mapping. All mappings must use this function."""
    return hash(frozenset(m.items()))


@Mapping.register
class FrozendictBase(Generic[K_co, V_co]):
    """Base class for immutable dictionaries. Unhashable, supports copy and pickle modules."""
    __slots__ = '_source',

    # region new overload
    @overload
    def __new__(cls, /) -> 'FrozendictBase': ...
    @overload
    def __new__(cls, /, **kwargs: V_co) -> 'FrozendictBase[str, V_co]': ...

    @overload
    def __new__(
            cls,
            mapping: SupportsKeysAndGetItem[K_co, V_co],
            /,
            ) -> 'FrozendictBase[K_co, V_co]': ...

    @overload
    def __new__(
            cls,
            mapping: SupportsKeysAndGetItem[str, V_co],
            /,
            **kwargs: V_co,
            ) -> 'FrozendictBase[str, V_co]': ...

    @overload
    def __new__(cls, iterable: Iterable[tuple[K_co, V_co]], /) -> 'FrozendictBase[K_co, V_co]': ...

    @overload
    def __new__(
            cls,
            iterable: Iterable[tuple[str, V_co]],
            /,
            **kwargs: V_co,
            ) -> 'FrozendictBase[str, V_co]': ...
    # endregion

    def __new__(cls, iterable = (), /, **kwargs):
        self = object.__new__(cls)
        self._source = dict(iterable, **kwargs)
        return self

    def __getnewargs__(self, /):
        return self._source,

    # region fromkeys overload
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[K_co], /) -> 'FrozendictBase[K_co, None]': ...
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[K_co], value: V_co, /) -> 'FrozendictBase[K_co, V_co]': ...
    # endregion

    @classmethod
    def fromkeys(cls, iterable, value = None, /) -> 'FrozendictBase':
        """Create a new dictionary with keys from ``iterable`` and values set to ``value``."""
        return cls((k, value) for k in iterable)

    def __getitem__(self, item: K_co, /) -> V_co:
        return self._source[item]

    # region get overload
    @overload
    def get(self, key: K_co, /) -> Optional[V_co]: ...
    @overload
    def get(self, key: K_co, default: V_co, /) -> V_co: ...
    @overload
    def get(self, key: K_co, default: T, /) -> Union[V_co, T]: ...
    # endregion

    def get(self, key, default = None, /):
        """Return the value for key if ``key`` is in the dictionary, else ``default``."""
        return self._source.get(key, default)

    def keys(self, /) -> KeysView[K_co]:
        """Return a set-like object providing a view on keys."""
        return self._source.keys()

    def values(self, /) -> ValuesView[V_co]:
        """Return an object providing a view on values."""
        return self._source.values()

    def items(self, /) -> ItemsView[K_co, V_co]:
        """Return a set-like object providing a view on key-value pairs."""
        return self._source.items()

    def __copy__(self, /):
        return self

    def __deepcopy__(self, memo: dict, /):
        # This method can return self if all values are hashable,
        # i.e., all values are immutable too.
        # But this requires a whole traverse through dict or hash value caching.
        # If such optimization is necessary, it can be used in a subclass.
        return self.__class__(deepcopy(self._source, memo))

    def __str__(self, /):
        return str(self._source)

    def __repr__(self, /):
        if len(self._source) == 0:
            return f'{self.__class__.__name__}()'

        return f'{self.__class__.__name__}({self._source})'

    def __len__(self, /):
        return len(self._source)

    def __contains__(self, item: Hashable, /):
        return item in self._source

    def __iter__(self, /) -> Iterator[K_co]:
        return iter(self._source)

    def __reversed__(self, /) -> Iterator[K_co]:
        return reversed(self._source)

    def __or__(self, other: Mapping[K_co, V_co], /) -> 'FrozendictBase[K_co, V_co]':
        if isinstance(other, Mapping):
            return self.__class__(chain(self._source.items(), other.items()))

        return NotImplemented

    def __ror__(self, other: Mapping[K_co, V_co], /) -> 'FrozendictBase[K_co, V_co]':
        if isinstance(other, Mapping):
            return self.__class__(chain(other.items(), self._source.items()))

        return NotImplemented

    # todo measure the speed of such implementation with simple self._source == other
    def __eq__(self, other: Any, /) -> bool:
        if isinstance(other, FrozendictBase):
            return self._source == other._source

        if isinstance(other, Mapping):
            return other == self._source

        return NotImplemented

    # todo measure the speed of such implementation with simple self._source != other
    def __ne__(self, other: Any, /) -> bool:
        if isinstance(other, FrozendictBase):
            return self._source != other._source

        if isinstance(other, Mapping):
            return other != self._source

        return NotImplemented

    def sizeof(self, /, gc_self: bool = True, gc_inner: bool = False) -> int:
        """Return the size of a dictionary in bytes.

        :param gc_self: If true, garbage collector overhead for itself is included.
        :param gc_inner: If true, garbage collector overhead for inner dictionary is included.
        """
        # It is better not to overwrite __sizeof__ method.
        # Instead, add a custom method.
        return (
                (getsizeof(self) if gc_self else self.__sizeof__())
                + (getsizeof(self._source) if gc_inner else self._source.__sizeof__())
        )


def get_hash_value_or_unhashable_type(mapping: Mapping, /) -> Union[int, str]:
    try:
        return mapping_hash(mapping)
    except TypeError as e:
        return str(e)[18:-1]


class frozendict(FrozendictBase[K_co, V_co]):
    """Subclass of :class:`FrozendictBase`. Hashable if all values are hashable.
    If hashable, hash value is cached after its first calculation."""
    __slots__ = '_hash',

    # region new overload
    @overload
    def __new__(cls, /) -> 'frozendict': ...
    @overload
    def __new__(cls, /, **kwargs: V_co) -> 'frozendict[str, V_co]': ...

    @overload
    def __new__(
            cls,
            mapping: SupportsKeysAndGetItem[K_co, V_co],
            /,
            ) -> 'frozendict[K_co, V_co]': ...

    @overload
    def __new__(
            cls,
            mapping: SupportsKeysAndGetItem[str, V_co],
            /,
            **kwargs: V_co,
            ) -> 'frozendict[str, V_co]': ...

    @overload
    def __new__(cls, iterable: Iterable[tuple[K_co, V_co]], /) -> 'frozendict[K_co, V_co]': ...

    @overload
    def __new__(
            cls,
            iterable: Iterable[tuple[str, V_co]],
            /,
            **kwargs: V_co,
            ) -> 'frozendict[str, V_co]': ...
    # endregion

    def __new__(cls, iterable = (), /, **kwargs):
        self = super().__new__(cls, iterable, **kwargs)
        self._hash = None
        return self

    def __hash__(self, /):
        if self._hash is None:
            self._hash = get_hash_value_or_unhashable_type(self._source)

        if isinstance(self._hash, int):
            return self._hash

        raise TypeError(f'unhashable type: {self._hash!r}')

    def __deepcopy__(self, memo, /):
        if self._hash is None:
            self._hash = get_hash_value_or_unhashable_type(self._source)

        if isinstance(self._hash, int):
            return self

        return self.__class__(deepcopy(self._source, memo))

    # region Overload for PyCharm
    # noinspection PyMethodOverriding
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[K_co], /) -> 'frozendict[K_co, None]': ...
    # noinspection PyMethodOverriding
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[K_co], value: V_co, /) -> 'frozendict[K_co, V_co]': ...
    @classmethod
    def fromkeys(cls, iterable, value = None, /) -> 'frozendict': ...

    def __or__(self, other: Mapping[K_co, V_co], /) -> 'frozendict[K_co, V_co]': ...
    def __ror__(self, other: Mapping[K_co, V_co], /) -> 'frozendict[K_co, V_co]': ...

    del fromkeys
    del __or__
    del __ror__
    # endregion
