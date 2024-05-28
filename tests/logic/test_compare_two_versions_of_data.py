import unittest

from src.logic import compare_two_versions_of_data


class TestFunc(unittest.TestCase):
    def test_same_keys(self):
        """
        Both inputs have the same keys, 'foo' and 'spam'
        """
        data1 = {"foo": "bar", "spam": "baz"}
        data2 = {"foo": "abc", "spam": "baz"}

        comparison = compare_two_versions_of_data(data1, data2)

        expected_comparison = [
            {
                "key": "foo",
                "action": "updated",
                "old_value": "bar",
                "new_value": "abc",
            },
            {
                "key": "spam",
                "action": "no change",
                "old_value": "baz",
                "new_value": "baz",
            },
        ]
        self.assertEqual(comparison, expected_comparison)

    def test_different_keys(self):
        """
        The two inputs have one key in common, 'foo', and one different key each.
        """
        data1 = {"foo": "bar", "spam": "baz"}  # 'spam' only exists in data1
        data2 = {"foo": "bar", "hello": 123}  # 'hello' is a new key in data2

        comparison = compare_two_versions_of_data(data1, data2)

        expected_comparison = [
            {
                "key": "foo",
                "action": "no change",
                "old_value": "bar",
                "new_value": "bar",
            },
            {
                "key": "hello",
                "action": "added",
                "old_value": None,
                "new_value": "123",
            },
            {
                "key": "spam",
                "action": "deleted",
                "old_value": "baz",
                "new_value": None,
            },
        ]

        self.assertEqual(comparison, expected_comparison)
