from peewee import SqliteDatabase, Model, PrimaryKeyField


class BasicModel(Model):
    """The migration model used to track migration status"""
    id = PrimaryKeyField()

    class Meta:
        database = SqliteDatabase('test.db')


def up():
    BasicModel.create_table(fail_silently=True)


def down():
    BasicModel.drop_table()
