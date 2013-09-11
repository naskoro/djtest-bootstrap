from testing import run_tests


class Command(object):
    option_list = []

    def run_from_argv(self, argv):
        import nose

        with run_tests():
            nose.main(argv[2:])
