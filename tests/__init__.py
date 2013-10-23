import unittest

from shift import _perform_migrations, _perform_single_migration
from shift.exceptions import (
    ModuleNotFoundException
)
from shift.models import Migration

from tests import example


class TestMigrationFunctions(unittest.TestCase):
    def setUp(self):
        self.model = Migration
        self.model._meta.database = example.DATABASE
        self.model.create_table()

    def tearDown(self):
        self.model.drop_table()

    def test_perform_single_migration(self):
        """A simple test of _perform_single_migration"""
        self.assertEqual(_perform_single_migration(
            example, "up", "001_initial", self.model
        ), True)

    def test_perform_single_migration_already_migrated(self):
        """Run migration twice, second time should return False"""
        self.assertEqual(_perform_single_migration(
            example, "up", "001_initial", self.model
        ), True)

        self.assertEqual(_perform_single_migration(
            example, "up", "001_initial", self.model
        ), False)

    def test_perform_single_migration_not_found(self):
        """Ensure that a bad migration argument raises an error"""
        with self.assertRaises(ModuleNotFoundException):
            _perform_single_migration(example, "up", "broken", self.model)

    def test_perform_migrations(self):
        """A simple test of _perform_migrations"""
        self.assertEqual(_perform_migrations(
            example, "up", self.model
        ), True)

    def test_perform_migrations_with_migration_argument(self):
        """A simple test of _perform_migrations with a migration argument"""
        self.assertEqual(_perform_migrations(
            example, "up", self.model, migration="001_initial"
        ), True)

if __name__ == '__main__':
    unittest.main()
