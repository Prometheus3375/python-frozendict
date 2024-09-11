# frozendict-x

`frozendict-x` is a library which provides a typed wrapper around dictionaries to protect them from 
updates and thus gain some other properties like being hashable.

Facts here must be added to complete readme!

frozendict не обязательно должен быть хешируемым, так как такое же поведение у tuple.
copy и deepcopy возвращают тот же объект, если он хешируем. Так ведёт tuple.
Однако deepcopy frozenset создаёт новый объект. (https://bugs.python.org/issue44703)

Use frozendict when you need immutable map with next properties:
- hashable
- subclassable
- supports copy and pickle modules
