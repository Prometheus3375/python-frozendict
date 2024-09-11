# mypy: ignore-errors
from collections.abc import ItemsView, Iterable, Iterator, KeysView, Mapping, ValuesView
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
    """
    Base class for immutable dictionaries.
    Unhashable, supports ``copy`` and ``pickle`` modules.
    """
    __slots__ = '__source',

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
    def __new__(
            cls,
            iterable: Iterable[tuple[K_co, V_co]],
            /
            ) -> 'FrozendictBase[K_co, V_co]': ...

    @overload
    def __new__(
            cls,
            iterable: Iterable[tuple[str, V_co]],
            /,
            **kwargs: V_co,
            ) -> 'FrozendictBase[str, V_co]': ...
    # endregion

    def __new__(cls, iterable = (), /, **kwargs):
        self = object.__new__(cls)  # todo check behaviour with multiple inheritance
        self.__source = dict(iterable, **kwargs)
        return self

    def __getnewargs__(self, /):
        return self.__source,

    # region fromkeys overload
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[K], /) -> 'FrozendictBase[K, None]': ...
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[K], value: T, /) -> 'FrozendictBase[K, T]': ...
    # endregion

    @classmethod
    def fromkeys(cls, iterable, value = None, /):
        """Create a new dictionary with keys from ``iterable`` and values set to ``value``."""
        return cls((k, value) for k in iterable)

    def __getitem__(self, item: K_co, /) -> V_co:
        return self.__source[item]

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
        return self.__source.get(key, default)

    def keys(self, /) -> KeysView[K_co]:
        """Return a set-like object providing a view on keys."""
        return self.__source.keys()

    def values(self, /) -> ValuesView[V_co]:
        """Return an object providing a view on values."""
        return self.__source.values()

    def items(self, /) -> ItemsView[K_co, V_co]:
        """Return a set-like object providing a view on key-value pairs."""
        return self.__source.items()

    def __copy__(self, /):
        return self

    def __deepcopy__(self, memo: dict, /):
        # This method can return self if all values are hashable,
        # i.e., all values are immutable too.
        # But this requires a whole traverse through dict or hash value caching.
        # If such optimization is necessary, it can be used in a subclass.
        return self.__class__(deepcopy(self.__source, memo))

    def __str__(self, /):
        return f'{self.__class__.__name__}({self.__source if self.__source else ""})'

    __repr__ = __str__

    def __len__(self, /):
        return len(self.__source)

    def __contains__(self, item: Any, /):
        # raises TypeError if item is not hashable
        return item in self.__source

    def __iter__(self, /) -> Iterator[K_co]:
        return iter(self.__source)

    def __reversed__(self, /) -> Iterator[K_co]:
        return reversed(self.__source)

    def __or__(self, other: Mapping[K, T], /) -> 'FrozendictBase[Union[K_co, K], Union[V_co, T]]':
        if isinstance(other, Mapping):
            return self.__class__(chain(self.__source.items(), other.items()))

        return NotImplemented

    def __ror__(self, other: Mapping[K, T], /) -> 'FrozendictBase[Union[K_co, K], Union[V_co, T]]':
        if isinstance(other, Mapping):
            return self.__class__(chain(other.items(), self.__source.items()))

        return NotImplemented

    def __eq__(self, other: Any, /) -> bool:
        return other == self.__source

    def __ne__(self, other: Any, /) -> bool:
        return other != self.__source

    def sizeof(self, /, gc_self: bool = True, gc_inner: bool = False) -> int:
        """Return the size of a dictionary in bytes.

        :param gc_self: If true, garbage collector overhead for itself is included.
        :param gc_inner: If true, garbage collector overhead for inner dictionary is included.
        """
        # It is better not to overwrite __sizeof__ method.
        # Instead, add a custom method.
        return (
                (getsizeof(self) if gc_self else self.__sizeof__())
                + (getsizeof(self.__source) if gc_inner else self.__source.__sizeof__())
        )


def get_hash_value_or_unhashable_type(mapping: Mapping, /) -> Union[int, str]:
    try:
        return mapping_hash(mapping)
    except TypeError as e:
        return str(e)[18:-1]


class frozendict(FrozendictBase[K_co, V_co]):
    """
    Subclass of :class:`FrozendictBase`. Hashable if all values are hashable.
    If hashable, hash value is cached after its first calculation.
    """
    __slots__ = '__hash',

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
    def __new__(
            cls,
            iterable: Iterable[tuple[K_co, V_co]],
            /
            ) -> 'frozendict[K_co, V_co]': ...

    @overload
    def __new__(
            cls,
            iterable: Iterable[tuple[str, V_co]],
            /,
            **kwargs: V_co,
            ) -> 'frozendict[str, V_co]': ...
    # endregion

    def __new__(cls, iterable = (), /, **kwargs):
        self = FrozendictBase.__new__(cls, iterable, **kwargs)
        # todo check behaviour with multiple inheritance
        self.__hash = None
        return self

    def __hash__(self, /):
        if self.__hash is None:
            self.__hash = get_hash_value_or_unhashable_type(self._FrozendictBase__source)

        if isinstance(self.__hash, int):
            return self.__hash

        raise TypeError(f'unhashable type: {self.__hash!r}')

    def __deepcopy__(self, memo, /):
        if self.__hash is None:
            self.__hash = get_hash_value_or_unhashable_type(self._FrozendictBase__source)

        if isinstance(self.__hash, int):
            return self

        return self.__class__(deepcopy(self._FrozendictBase__source, memo))

    # region Overload for PyCharm
    # noinspection PyMethodOverriding
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[K], /) -> 'frozendict[K, None]': ...
    # noinspection PyMethodOverriding
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[K], value: T, /) -> 'frozendict[K, T]': ...
    @classmethod
    def fromkeys(cls, iterable, value = None, /): ...

    def __or__(self, other: Mapping[K, T], /) -> 'frozendict[Union[K_co, K], Union[V_co, T]]': ...
    def __ror__(self, other: Mapping[K, T], /) -> 'frozendict[Union[K_co, K], Union[V_co, T]]': ...

    del fromkeys
    del __or__
    del __ror__
    # endregion
