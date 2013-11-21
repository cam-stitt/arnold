from peewee import SqliteDatabase, Model, PrimaryKeyField

db = SqliteDatabase('test.db')


class BasicModel(Model):
    """The migration model used to track migration status"""
    id = PrimaryKeyField()

    class Meta:
        database = db


def up():
    BasicModel.create_table(fail_silently=True)


def down():
    BasicModel.drop_table()
