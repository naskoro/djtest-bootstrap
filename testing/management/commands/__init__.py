import os
from contextlib import contextmanager

from django.db import connection
from django.test.utils import setup_test_environment, teardown_test_environment


@contextmanager
def run_tests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ptest.settings'
    setup_test_environment()
    connection.creation.create_test_db(verbosity=0, autoclobber=True)
    try:
        yield
    finally:
        teardown_test_environment()
