
import builtins
import unittest
from mock import Mock, patch, mock_open

from ..file import TextFile


class TestPublish(unittest.TestCase):

    F = TextFile('output.txt')

    def test_set(self):
        self.F.set(a=1, b=2, c=3)
        self.assertEqual(self.F.args, {'a': 1, 'b': 2, 'c': 3})
        self.F.set(c=1, d=2, e=3)
        self.assertEqual(self.F.args, {'c': 1, 'd': 2, 'e': 3})

    def test_positional_set(self):
        self.assertRaises(TypeError, self.F.set, 1, 2, 3)

    def test_single_value(self):
        m = mock_open()
        with patch.object(builtins, 'open', m):
            self.F.set(a=1)
            self.F.publish()

            m.assert_called()
            handle = m()
            handle.write.assert_called_with('a 1\n')

    def test_string_value(self):
        m = mock_open()
        with patch.object(builtins, 'open', m):
            self.F.set(a='string arg')
            self.F.publish()

            m.assert_called()
            handle = m()
            handle.write.assert_called_with("a 'string arg'\n")

    def test_list_value(self):
        m = mock_open()
        with patch.object(builtins, 'open', m):
            self.F.set(a=[1, 2, 3])
            self.F.publish()

            m.assert_called()
            handle = m()
            handle.write.assert_called_with("a 1 2 3\n")

    def test_double_list_value(self):
        m = mock_open()
        with patch.object(builtins, 'open', m):
            self.F.set(a=[['a', 'b', 'c'], 2, 3])
            self.F.publish()

            m.assert_called()
            handle = m()
            handle.write.assert_called_with("a 'a' 'b' 'c' 2 3\n")
