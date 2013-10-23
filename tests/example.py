from peewee import SqliteDatabase

DATABASE = SqliteDatabase('test.db')

MIGRATION_DIR = "tests/migrations"
MIGRATION_MODULE = "tests.migrations"
