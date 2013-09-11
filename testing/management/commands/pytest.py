from . import run_tests


class Command(object):
    option_list = []

    def run_from_argv(self, argv):
        import pytest

        with run_tests():
            nose2.main(argv[2:])
