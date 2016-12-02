from __future__ import print_function
import logging
from unittest import TestCase
from checkrunner import CheckRunner

__author__ = 'al4'
# logging.basicConfig(level=logging.DEBUG)


class ExampleChecks(object):
    """ Example checks which we use in the tests """
    @classmethod
    def passing_check(cls):
        return True, 'this check always passes :)'

    @classmethod
    def failing_check(cls):
        return False, 'this check always fails'

    @classmethod
    def exception_raising_check(cls):
        raise Exception('test exception')

    @classmethod
    def _private_method(cls):
        """ We should always exclude private methods """
        raise NotImplementedError("This should never be run")


class CommonTests(object):
    my_class = None

    def test_returns_tuple(self):
        self.assertIsInstance(self.my_class.run(), tuple)

    def test_first_return_arg_is_boolean(self):
        self.assertIsInstance(self.my_class.run()[0], bool)

    def test_second_return_arg_is_list(self):
        self.assertIsInstance(self.my_class.run()[1], list)


class FailureTests(object):
    """ Test the failure scenarios """
    my_class = None

    def test_list_is_not_empty(self):
        self.assertEqual(
            len(self.my_class.run()[1]),
            1
        )

    def test_list_contains_failed(self):
        """ Test the list contains our fail string """
        self.assertEqual(
            self.my_class.run()[1][0],
            'this check always fails'
        )


# Testing the common tests against the various cases (all passing, all failing,
# mixed)
class TestPassing(TestCase, CommonTests):
    """ All checks pass """
    class PassingChecks(CheckRunner):
        passing_check = ExampleChecks.passing_check
    my_class = PassingChecks

    def test_list_is_empty(self):
        self.assertListEqual(self.my_class.run()[1], [])


class TestFailing(TestCase, CommonTests, FailureTests):
    """ All checks fail """
    class FailingChecks(CheckRunner):
        failing_check = ExampleChecks.failing_check
    my_class = FailingChecks


class TestMixed(TestCase, CommonTests, FailureTests):
    """ Both passing and failing checks """
    class MixedChecks(CheckRunner):
        passing_check = ExampleChecks.passing_check
        failing_check = ExampleChecks.failing_check

    my_class = MixedChecks

    def test_mixed_returns_false(self):
        """ Result of a test with some failed checks is fail """
        result, out = self.my_class.run()
        self.assertFalse(result)

    def test_mixed_returns_only_failed(self):
        result, out = self.my_class.run()
        self.assertEqual(len(out), 1)


class TestPrivateMethods(TestCase, CommonTests):
    """ Tests with a private method present
    """
    class MyChecks(CheckRunner):
        passing_check = ExampleChecks.passing_check
        failing_check = ExampleChecks.failing_check
        _excluded_method = ExampleChecks._private_method

    my_class = MyChecks

    def test_get_methods_excludes_private(self):
        """ Test that we exclude private methods
        """
        methods = self.my_class._get_check_methods()
        self.assertNotIn(self.my_class._excluded_method, methods)
