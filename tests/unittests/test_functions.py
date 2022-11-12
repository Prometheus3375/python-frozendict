from unittest import TestCase

from frozendictx import mapping_hash


class MappingHash(TestCase):
    """
    This test case must be run with environmental variable ``PYTHONHASHSEED`` set to zero.
    """
    def test_empty(self, /):
        """Checks hash value for empty mapping"""
        d = {}

        value = mapping_hash(d)
        self.assertEqual(133146708735736, value, f'Current hash: {value!r}')

    def test_5(self, /):
        """Checks hash value for 5-sized mapping"""
        d = dict(one=1, two=2, three=3, four=4, five=5)

        value = mapping_hash(d)
        self.assertEqual(3919848624938419493, value, f'Current hash: {value!r}')

    def test_10(self, /):
        """Checks hash value for 10-sized mapping"""
        d = dict(one=1, two=2, three=3, four=4, five=5, six=6, seven=7, eight=8, nine=9, ten=10)

        value = mapping_hash(d)
        self.assertEqual(value, 8718668387893418241, f'Current hash: {value!r}')

    def test_5r(self, /):
        """Checks hash value for 5-sized mapping with swapped keys and values"""
        d = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}

        value = mapping_hash(d)
        self.assertEqual(value, 5917240795287630226, f'Current hash: {value!r}')

    def test_10r(self, /):
        """Checks hash value for 10-sized mapping with swapped keys and values"""
        d = {
            1: 'one',
            2: 'two',
            3: 'three',
            4: 'four',
            5: 'five',
            6: 'six',
            7: 'seven',
            8: 'eight',
            9: 'nine',
            10: 'ten'
            }

        value = mapping_hash(d)
        self.assertEqual(value, 5003416146848621781, f'Current hash: {value!r}')
