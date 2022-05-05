from frozendictx._frozendict import FrozendictBase, frozendict


def base_creation():
    d1 = FrozendictBase()  # FrozendictBase | FrozendictBase[str, Any]
    d2 = FrozendictBase(one=1)  # FrozendictBase[str, int]
    d3 = FrozendictBase({'one': 1})  # FrozendictBase[str, int]
    d4 = FrozendictBase({1: 'one'})  # FrozendictBase[int, str]
    d5 = FrozendictBase({'one': 1}, two=2)  # FrozendictBase[str, int]
    d6 = FrozendictBase({1: 'one'}, two=2)  # Unexpected type(s)
    d7 = FrozendictBase([('one', 1), ('two', 2)])  # FrozendictBase[str, int]
    d8 = FrozendictBase([(1, 'one'), (2, 'two')])  # FrozendictBase[int, str]
    d9 = FrozendictBase([('one', 1), ('two', 2)], three=3)  # FrozendictBase[str, int]
    d10 = FrozendictBase([(1, 'one'), (2, 'two')], three=3)  # Unexpected type(s)


def base_fromkeys():
    d1 = FrozendictBase.fromkeys([1, 2, 3, 4, 5, 6])  # FrozendictBase[int, None]
    d2 = FrozendictBase.fromkeys([1, 2, 3, 4, 5, 6], 'value')  # FrozendictBase[int, str]


def base_get():
    d = FrozendictBase([('one', 1), ('two', 2)], three=3)
    v0 = d[1]  # Expected type 'str'
    v1 = d['one']  # int
    v2 = d.get(1)  # Expected type 'str'
    v3 = d.get('two')  # int | None
    v4 = d.get('one', 0)  # int
    v5 = d.get('two', '')  # int | str


def base_views():
    d = FrozendictBase([('one', 1), ('two', 2)], three=3)
    keys = d.keys()  # KeysView[str]
    values = d.values()  # ValuesView[int]
    items = d.items()  # ItemsView[str, int]


def base_in():
    d = FrozendictBase([('one', 1), ('two', 2)], three=3)
    v0 = 5 in d  # bool
    v1 = '' in d  # bool
    v2 = set() in d  # bool

    for k1 in d: ...  # str
    for k2 in iter(d): ...  # str
    for k3 in reversed(d): ...  # str


def base_or():
    d1 = FrozendictBase([('one', 1), ('two', 2)], three=3)
    d2 = FrozendictBase([('one', 1), ('two', 2)], three=3)
    d3 = FrozendictBase.fromkeys([1, 2, 3, 4, 5, 6], 'value')
    d4 = d1 | d2  # FrozendictBase[str, int]
    d5 = d1 | d3  # Expected type 'Mapping[str, int]'


def base_eq():
    d1 = FrozendictBase([('one', 1), ('two', 2)], three=3)
    d2 = FrozendictBase([('one', 1), ('two', 2)], three=3)
    d3 = FrozendictBase.fromkeys([1, 2, 3, 4, 5, 6], 'value')
    b1 = d1 == d2  # bool
    b2 = d1 != d2  # bool
    b3 = d1 == d3  # bool
    b4 = d1 != d3  # bool


def frozendict_creation():
    d1 = frozendict()  # frozendict | frozendict[str, Any]
    d2 = frozendict(one=1)  # frozendict[str, int]
    d3 = frozendict({'one': 1})  # frozendict[str, int]
    d4 = frozendict({1: 'one'})  # frozendict[int, str]
    d5 = frozendict({'one': 1}, two=2)  # frozendict[str, int]
    d6 = frozendict({1: 'one'}, two=2)  # Unexpected type(s)
    d7 = frozendict([('one', 1), ('two', 2)])  # frozendict[str, int]
    d8 = frozendict([(1, 'one'), (2, 'two')])  # frozendict[int, str]
    d9 = frozendict([('one', 1), ('two', 2)], three=3)  # frozendict[str, int]
    d10 = frozendict([(1, 'one'), (2, 'two')], three=3)  # Unexpected type(s)


def frozendict_fromkeys():
    d1 = frozendict.fromkeys([1, 2, 3, 4, 5, 6])  # frozendict[int, None]
    d2 = frozendict.fromkeys([1, 2, 3, 4, 5, 6], 'value')  # frozendict[int, str]


def frozendict_or():
    d1 = frozendict([('one', 1), ('two', 2)], three=3)
    d2 = frozendict([('one', 1), ('two', 2)], three=3)
    d3 = frozendict.fromkeys([1, 2, 3, 4, 5, 6], 'value')
    d4 = d1 | d2  # frozendict[str, int]
    d5 = d1 | d3  # Expected type 'Mapping[str, int]'


def interclass_or():
    d1 = FrozendictBase([('one', 1), ('two', 2)], three=3)
    d2 = frozendict([('one', 1), ('two', 2)], three=3)
    d3 = d1 | d2  # FrozendictBase[str, int] | frozendict[str, int]
    d4 = d2 | d1  # frozendict[str, int] | FrozendictBase[str, int]
