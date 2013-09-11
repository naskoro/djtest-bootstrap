from testing import run_tests


class Command(object):
    option_list = []

    def run_from_argv(self, argv):
        import nose2

        with run_tests():
            nose2.main(module=None, argv=argv[1:])
