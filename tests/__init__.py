import os
import sys
import unittest

from peewee import SqliteDatabase, Model

from arnold import Terminator, parse_args
from arnold.models import Migration

#sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

db = SqliteDatabase('test.db')


class BasicModel(Model):
    pass


class TestMigrationFunctions(unittest.TestCase):
    def setUp(self):
        self.model = Migration
        self.model._meta.database = db
        if self.model.table_exists():
            self.model.drop_table()
        self.model.create_table()

        self.good_migration = "001_initial"
        self.bad_migration = "bad"

    def tearDown(self):
        self.model.drop_table()
        BasicModel.drop_table(fail_silently=True)

    def test_setup_table(self):
        """Ensure that the Migration table will be setup properly"""
        # Drop the table if it exists, as we are creating it later
        if self.model.table_exists():
            self.model.drop_table()
        args = parse_args(['status'])
        Terminator(args)
        self.assertEqual(self.model.table_exists(), True)

    def do_good_migration_up(self):
        """A utility to perform a successfull upwards migration"""
        args = parse_args(['up', '1'])
        termi = Terminator(args)
        termi.perform_migrations('up')
        self.assertTrue("basicmodel" in db.get_tables())

    def do_good_migration_down(self):
        """A utility to perform a successfull downwards migration"""
        args = parse_args(['down', '1'])
        termi = Terminator(args)
        termi.perform_migrations('down')
        self.assertFalse("basicmodel" in db.get_tables())

    def test_perform_single_migration(self):
        """A simple test of _perform_single_migration"""
        self.do_good_migration_up()

    def test_perform_single_migration_already_migrated(self):
        """Run migration twice, second time should return False"""
        self.do_good_migration_up()

        args = parse_args(['up', '1'])
        termi = Terminator(args)
        self.assertFalse(termi.perform_migrations('up'))

    def test_perform_single_migration_not_found(self):
        """Ensure that a bad migration argument raises an error"""
        args = parse_args(['up', '1'])
        termi = Terminator(args)

        with self.assertRaises(ImportError):
            termi.direction = 'up'
            termi._perform_single_migration('up')

    def test_perform_single_migration_down(self):
        """A simple test of _perform_single_migration down"""
        self.do_good_migration_up()

        self.do_good_migration_down()

    def test_perform_single_migration_down_does_not_exist(self):
        """Ensure False response when migration isn't there"""
        args = parse_args(['down', '1'])
        termi = Terminator(args)

        self.assertFalse(termi.perform_migrations('down'))

    def test_perform_single_migration_adds_deletes_row(self):
        """Make sure that the migration rows are added/deleted"""
        self.do_good_migration_up()

        self.assertTrue(self.model.select().where(
            self.model.migration == self.good_migration
        ).limit(1).exists())

        self.do_good_migration_down()

        self.assertFalse(self.model.select().where(
            self.model.migration == self.good_migration
        ).limit(1).exists())

    def test_with_fake_argument_returns_true_no_table(self):
        """If we pass fake, return true, but don't create the model table"""
        args = parse_args(['up', '1', '--fake', 'true'])
        termi = Terminator(args)
        self.assertTrue(termi.perform_migrations('up'))
        self.assertFalse("basicmodel" in db.get_tables())

if __name__ == '__main__':
    unittest.main()
