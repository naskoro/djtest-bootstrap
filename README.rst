Bootstrap multiprocess tests
============================
**NB:** Support transaction tests.

**Tested with postgresql and sqlite.** Look at ``DATABASES`` in ``"ptest/settings.py"``.

Run test with multiprocess via ``nose``, ``nose2`` or ``pytest``.
Use little bit of code for it::

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
        from testing import run_tests


    ### testing/management/commands/pytest.py ###
    from testing import run_tests


    class Command(object):
        option_list = []

        def run_from_argv(self, argv):
            import pytest

            with run_tests():
                pytest.main(argv[2:])

Example of using different runner::

    # pytest
    $ ./manage.py pytest testing/tests/test_v1.py -n3

    # nose
    $ ./manage.py nose testing/tests/test_v1.py -N3
    $ ./manage.py nose testing.tests.test_v1 --processes=3
    $ ./manage.py nose testing --processes=3 --process-timeout=300

    # nose2
    $ ./manage.py nose2 testing.tests.test_v1 --processes=3

**Warning:** Need tuning ``nose`` and ``nose2`` support.


Some measures
-------------
Repository has some synthetic tests in ``"testing/tests"`` for trying.

**NB:** Postgresql used as database backend.

Try on **all (216)** tests::

    ## Ran 216 tests

    # 1 process
    $ ./manage.py pytest testing
        122.77s user 0.56s system 97% cpu 2:06.26 total

    # 3 process
    $ ./manage.py pytest testing -n3
        42.28s user 0.25s system 42% cpu 1:41.26 total
    $ ./manage.py nose testing --processes=3 --process-timeout=300
        140.27s user 0.71s system 137% cpu 1:42.53 total
    $ ./manage.py nose2 testing --processes=3
        133.31s user 0.59s system 128% cpu 1:44.03 total

Try only **24** tests::

    ## Ran 24 tests

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

Maybe need more measures, but even that results it is good point for understanding.
