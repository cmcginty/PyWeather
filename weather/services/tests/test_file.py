from __future__ import absolute_import

import unittest
from mock import Mock, patch_object, patch, sentinel

from ..file import TextFile

class TestPublish(unittest.TestCase):

   F = TextFile('output.txt')

   def test_set(self):
      self.F.set( a=1, b=2, c=3 )
      self.assertEquals( self.F.args, {'a':1,'b':2,'c':3} )
      self.F.set( c=1, d=2, e=3 )
      self.assertEquals( self.F.args, {'c':1,'d':2,'e':3} )

   def test_positional_set(self):
      self.assertRaises( TypeError, self.F.set, 1,2,3)

   def _set_open_mock(self):
      file_mock = Mock()
      ctx_mock = Mock(open)
      exit_mock = Mock()
      enter_mock = Mock()
      enter_mock.return_value = file_mock
      setattr(ctx_mock,'__exit__',exit_mock)
      setattr(ctx_mock,'__enter__',enter_mock)
      return ctx_mock

   @patch('__builtin__.open' )
   def test_single_value(self, open_mock):
      # setup
      open_mock.return_value = self._set_open_mock()

      # test
      self.F.set( a=1 )
      self.F.publish()

      exit = open_mock.return_value.__exit__
      file_ = open_mock.return_value.__enter__.return_value
      self.assertEquals( exit.called, 1 )
      self.assertEquals( exit.call_args, ((None,None,None), {}) )
      self.assertEquals( file_.write.call_args, (('a 1\n',),{})  )

   @patch('__builtin__.open' )
   def test_string_value(self, open_mock):
      # setup
      open_mock.return_value = self._set_open_mock()

      # test
      self.F.set( a='string arg' )
      self.F.publish()

      exit = open_mock.return_value.__exit__
      file_ = open_mock.return_value.__enter__.return_value
      self.assertEquals( exit.called, 1 )
      self.assertEquals( exit.call_args, ((None,None,None), {}) )
      self.assertEquals( file_.write.call_args, (("a 'string arg'\n",),{})  )

   @patch('__builtin__.open' )
   def test_list_value(self, open_mock):
      # setup
      open_mock.return_value = self._set_open_mock()

      # test
      self.F.set( a=[1,2,3] )
      self.F.publish()

      exit = open_mock.return_value.__exit__
      file_ = open_mock.return_value.__enter__.return_value
      self.assertEquals( exit.called, 1 )
      self.assertEquals( exit.call_args, ((None,None,None), {}) )
      self.assertEquals( file_.write.call_args, (("a 1 2 3\n",),{})  )

   @patch('__builtin__.open' )
   def test_double_list_value(self, open_mock):
      # setup
      open_mock.return_value = self._set_open_mock()

      # test
      self.F.set( a=[['a','b','c'],2,3] )
      self.F.publish()

      exit = open_mock.return_value.__exit__
      file_ = open_mock.return_value.__enter__.return_value
      self.assertEquals( exit.called, 1 )
      self.assertEquals( exit.call_args, ((None,None,None), {}) )
      self.assertEquals( file_.write.call_args, (("a 'a' 'b' 'c' 2 3\n",),{})  )
