from peewee import SqliteDatabase
import migrations

database = SqliteDatabase('test.db')
migration_module = migrations
directory = './migrations'

