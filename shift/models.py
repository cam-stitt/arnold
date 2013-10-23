import datetime

from peewee import CharField, DateTimeField, Model, PrimaryKeyField


class Migration(Model):
    """The migration model used to track migration status"""
    id = PrimaryKeyField()
    migration = CharField(max_length=255)
    applied_on = DateTimeField(default=datetime.datetime.now)
