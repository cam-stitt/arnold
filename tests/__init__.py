import unittest

from peewee import SqliteDatabase

from shift import _perform_migrations, _perform_single_migration, main
from shift.exceptions import (
    ModuleNotFoundException
)
from shift.models import Migration


db = SqliteDatabase('test.db')

directory = "tests/migrations"
migration_module = "tests.migrations"

kwargs = {
    'directory': directory,
    'migration_module': migration_module
}


class TestMigrationFunctions(unittest.TestCase):
    def setUp(self):
        self.model = Migration
        self.model._meta.database = db
        if self.model.table_exists():
            self.model.drop_table()
        self.model.create_table()

    def tearDown(self):
        self.model = Migration
        self.model._meta.database = db
        self.model.drop_table()

    def test_perform_single_migration(self):
        """A simple test of _perform_single_migration"""
        self.assertEqual(_perform_single_migration(
            "up", self.model, migration="001_initial", **kwargs
        ), True)

    def test_perform_single_migration_already_migrated(self):
        """Run migration twice, second time should return False"""
        self.assertEqual(_perform_single_migration(
            "up", self.model, migration="001_initial", **kwargs
        ), True)

        self.assertEqual(_perform_single_migration(
            "up", self.model, migration="001_initial", **kwargs
        ), False)

    def test_perform_single_migration_not_found(self):
        """Ensure that a bad migration argument raises an error"""
        with self.assertRaises(ModuleNotFoundException):
            _perform_single_migration(
                "up", self.model, migration="broken", **kwargs
            )

    def test_perform_migrations(self):
        """A simple test of _perform_migrations"""
        self.assertEqual(_perform_migrations(
            "up", self.model, **kwargs
        ), True)

    def test_perform_migrations_with_migration_argument(self):
        """A simple test of _perform_migrations with a migration argument"""
        self.assertEqual(_perform_migrations(
            "up", self.model, migration="001_initial", **kwargs
        ), True)

    def test_single_migration_through_main(self):
        """Call shift's main method and perform a single migration"""
        self.assertEqual(main(
            database=db, **kwargs
        ), True)

if __name__ == '__main__':
    unittest.main()
