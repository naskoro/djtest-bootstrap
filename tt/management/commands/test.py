from django.conf import settings
from django.db import connection
from django.test.utils import setup_test_environment, teardown_test_environment

db_conf = settings.DATABASES['default']


class Command(object):
    option_list = []

    def run_from_argv(self, argv):
        import os
        import pytest

        os.environ['DJANGO_SETTINGS_MODULE'] = 'ptest.settings'
        setup_test_environment()
        connection.creation.create_test_db(verbosity=0, autoclobber=True)
        try:
            pytest.main(argv[2:])
        finally:
            teardown_test_environment()
