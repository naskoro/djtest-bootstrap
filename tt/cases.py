import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction, connection, DatabaseError
from django.test import TestCase as _TestCase
from mock import patch

logger = logging.getLogger('debug')


class TestCase(_TestCase):
    def mock_transaction_methods(self):
        def fake(*args, **kwargs):
            raise AssertionError(
                'Can\'t use transaction mode. Use "db_unique=True"'
            )

        methods = [
            'commit', 'rollback', 'managed',
            'enter_transaction_management', 'leave_transaction_management'
        ]
        mocks = []
        for method in methods:
            mok = patch.object(transaction, method, fake)
            mok.start()
            mocks.append(mok)
        self._transaction_mocks = mocks

    def fix_db(self):
        for db in settings.DATABASES.values():
            if db['NAME'] == ':memory:':
                continue
            elif 'TEST_NAME' in db:
                continue
            test_name = connection.creation._get_test_db_name()
            db['NAME'] = test_name
            db['TEST_NAME'] = test_name

        try:
            User.objects.count()
        except DatabaseError:
            logger.debug('Create test database')
            connection.creation.create_test_db(verbosity=0, autoclobber=True)

    def _fixture_setup(self):
        self.fix_db()
        transaction.enter_transaction_management()
        transaction.managed(True)
        self.mock_transaction_methods()

    def _fixture_teardown(self):
        for mok in self._transaction_mocks:
            mok.stop()

        transaction.rollback()
        transaction.leave_transaction_management()
