Bootstrap multiprocess tests
============================
**NB:** Support transaction tests only.

**Tested with postgresql and sqlite.** Look at ``DATABASES`` in ``"ptest/settings.py"``.

Run test with multiprocess via ``nose``, ``nose2`` or ``pytest``.

Example of using different runner::

    # pytest
    $ ./manage.py pytest testing/tests/test_v1.py -n3

    # nose
    $ ./manage.py nose testing/tests/test_v1.py -N3
    $ ./manage.py nose testing.tests.test_v1 --processes=3
    $ ./manage.py nose testing --processes=3 --process-timeout=300

    # nose2
    $ ./manage.py nose2 testing.tests.test_v1 --processes=3

Used little bit of code for that::

    $ ll testing
        4.0K management/
        4.0K tests/
         428 __init__.py
        1.7K cases.py

    $ ll testing/management/commands/
          0 __init__.py
        191 nose.py
        211 nose2.py
        195 pytest.py

**Warning:** Need to improve ``nose`` and ``nose2`` support.

Example of ``pytest`` command:

.. code:: py

    ### testing/__init__.py ###
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


    ### testing/management/commands/pytest.py ###
    from testing import run_tests


    class Command(object):
        option_list = []

        def run_from_argv(self, argv):
            import pytest

            with run_tests():
                pytest.main(argv[2:])

Some measurements
-----------------
Repository has some synthetic tests in ``"testing/tests"`` for trying.

System configuration
  ::

    Intel Core i5-3210M, SSD, Mem~8G
    Kernel~3.10.5-1-ARCH x86_64

    PostgreSQL 9.2.4; fsync=off
    Python 3.3.2
    Django 1.5.3

With PostgreSQL
~~~~~~~~~~~~~~~

Try only **24** tests::

    # 1 process
    $ ./manage.py pytest testing/tests/test_v1.py
        14.26s user 0.12s system 95% cpu 15.059 total
    $ ./manage.py nose testing.tests.test_v1
        14.21s user 0.12s system 95% cpu 14.995 total
    $ ./manage.py nose2 testing.tests.test_v1
        14.31s user 0.06s system 95% cpu 15.041 total

    # 3 process
    $ ./manage.py pytest testing/tests/test_v1.py -n3
        10.05s user 0.12s system 76% cpu 13.356 total
    $ ./manage.py nose testing.tests.test_v1 --processes=3 --process-timeout=300
        15.76s user 0.16s system 122% cpu 12.968 total
    $ ./manage.py nose2 testing.tests.test_v1 --processes=3
        15.46s user 0.12s system 130% cpu 11.942 total

Try on **all 216** tests::

    # 1 process
    $ ./manage.py pytest testing
        122.77s user 0.56s system 97% cpu 2:06.26 total
    $ ./manage.py nose testing
        123.16s user 0.52s system 97% cpu 2:06.48 total
    $ ./manage.py nose2 testing
        122.16s user 0.60s system 97% cpu 2:05.57 total

    # 3 process
    $ ./manage.py pytest testing -n3
        42.28s user 0.25s system 42% cpu 1:41.26 total
    $ ./manage.py nose testing --processes=3 --process-timeout=300
        140.27s user 0.71s system 137% cpu 1:42.53 total
    $ ./manage.py nose2 testing --processes=3
        133.31s user 0.59s system 128% cpu 1:44.03 total

    # 2 process
    $ ./manage.py pytest testing -n2
        65.44s user 0.38s system 64% cpu 1:41.59 total

    # 4 process
    $ ./manage.py pytest testing -n4
        42.87s user 0.26s system 41% cpu 1:42.90 total

    # 5 process
    $ ./manage.py pytest testing -n5
        28.73s user 0.20s system 28% cpu 1:42.65 total

With SQLite
~~~~~~~~~~~

Try on **all 216** tests::

    # 1 process
    ./manage.py pytest testing
        120.49s user 0.39s system 100% cpu 2:00.75 total
    $ ./manage.py nose testing
        122.29s user 0.30s system 100% cpu 2:02.45 total
    $ ./manage.py nose2 testing
        123.15s user 0.38s system 100% cpu 2:03.39 total

    # 4 process
    $ ./manage.py pytest testing -n4
        61.37s user 0.29s system 96% cpu 1:03.58 total
    $ ./manage.py nose testing --processes=4
        246.00s user 0.85s system 383% cpu 1:04.41 total
    $ ./manage.py nose2 testing -N4
        197.82s user 0.57s system 305% cpu 1:04.86 total

    # 3 process
    $ ./manage.py pytest testing -n3
        65.42s user 0.27s system 99% cpu 1:06.29 total

    # 2 process
    $ ./manage.py pytest testing -n2
        67.34s user 0.25s system 99% cpu 1:07.91 total

Maybe need more measurements, but even these results give us good starting point for
understanding.
