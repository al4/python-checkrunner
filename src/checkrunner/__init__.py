from __future__ import print_function
import logging

__author__ = 'al4'
logger = logging.getLogger(__name__)


class CheckRunner(object):
    """ Execute a suite of checks
    """
    @classmethod
    def run(cls):
        methods = cls._get_check_methods()
        logger.debug('Found methods: {}'.format([
            m.__name__ for m in methods
        ]))
        results = []

        for check_function in methods:
            logger.debug('Running check_function {}'.format(
                check_function.__name__))
            results.append(check_function())

        logger.debug('Results: {}'.format(results))
        if all([result for result, message in results]) \
                or not results:
            # All are true or empty list
            logger.debug('All checks passed')
            return True, []
        else:
            failed = [message for result, message in results if result is False]
            logger.debug('Checks failed: {}'.format(failed))
            return False, failed

    @classmethod
    def _get_check_methods(cls):
        """
        Fetch the methods declared in this class by comparing to the base class

        We exclude private methods (that start with an underscore)
        """

        my_class = None
        for subclass in CheckRunner.__subclasses__():
            if subclass.__name__ == cls.__name__:
                my_class = subclass

        if not my_class:
            # not a subclass?
            return []
        else:
            methods = list(set(dir(my_class)) - set(dir(CheckRunner)))
            logger.debug('All methods: {}'.format(methods))
            return [
                getattr(cls, m) for m in methods if not m.startswith('_')
            ]

