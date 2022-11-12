from copy import deepcopy
from unittest import TestCase

from frozendictx import frozendict


class Deepcopy(TestCase):
    def test_empty(self, /):
        """Tests if empty frozendict instance returns itself on deepcopy"""
        fd = frozendict()

        self.assertIs(fd, deepcopy(fd))

    def test_hashable(self, /):
        """Tests if hashable frozendict instance returns itself on deepcopy"""
        fd = frozendict(one=1, two=2, three=3, four=4, five=5)

        self.assertIs(fd, deepcopy(fd))

    def test_unhashable(self, /):
        """Tests if unhashable frozendict instance returns a new instance on deepcopy"""
        fd = frozendict(one=[1], two=[2], three=[3], four=[4], five=[5])

        self.assertIsNot(fd, deepcopy(fd))


class Hash(TestCase):
    """
    This test case must be run with environmental variable ``PYTHONHASHSEED`` set to zero.
    """
    def try_hash(self, fd: frozendict, /):
        self.assertIs(fd._frozendict__hash, None)

        try: hash(fd)
        except TypeError: pass

        self.assertIsNot(fd._frozendict__hash, None)

        return fd._frozendict__hash

    def test_empty(self, /):
        """Checks cached hash value of empty frozendict instance"""
        fd = frozendict()

        value = self.try_hash(fd)
        self.assertEqual(133146708735736, value, f'Current hash: {value!r}')

    def test_hashable(self, /):
        """Checks cached hash value of hashable frozendict instance"""
        fd = frozendict(one=1, two=2, three=3, four=4, five=5)

        value = self.try_hash(fd)
        self.assertEqual(3919848624938419493, value, f'Current hash: {value!r}')

    def test_unhashable(self, /):
        """Checks cached hash value of unhashable frozendict instance"""
        fd = frozendict(one=[1], two=[2], three=[3], four=[4], five=[5])

        value = self.try_hash(fd)
        self.assertEqual('list', value, f'Current hash: {value!r}')
