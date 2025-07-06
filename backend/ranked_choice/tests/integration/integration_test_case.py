import os
import django
from django.test import TestCase
from django.conf import settings
from django.core.management import call_command
from django.db import connections

# Configure database settings at module level before any tests run
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ranked_choice.settings')

# This class provides a base for integration tests that need a test database
class IntegrationTestCase(TestCase):
    """
    Base test case for integration tests that require a database.
    This class sets up a test database and runs migrations.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment before any tests are run.
        """
        # Database configuration is now handled in conftest.py
        # Call parent setUpClass
        super().setUpClass()

    def setUp(self):
        """
        Set up before each test.
        """
        # Verify that we're using the test database
        db_name = connections['default'].settings_dict['NAME']
        db_engine = connections['default'].settings_dict['ENGINE']

        # Allow both PostgreSQL test databases and SQLite in-memory databases
        is_test_db = db_name.startswith('test_') or db_name == ':memory:' or 'sqlite' in db_engine
        if not is_test_db:
            self.fail(f"Tests are not using a test database! Current database: {db_name} with engine {db_engine}")
        super().setUp()

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after all tests have run.
        """
        # Call parent tearDownClass
        super().tearDownClass()
