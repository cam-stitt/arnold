Creating Migrations
-------------------

Migrations are easy to setup. Simply create a `migration` folder
(with an `__init__.py`) and then start creating your migrations.

Migrations require two methods. `up` for creation and `down` for deletion.

Peewee has the ability to easily perform migrations such as adding a column. See `peewee docs <http://peewee.readthedocs.org/en/latest/peewee/playhouse.html#basic-schema-migrations>`_.

You must follow the naming convention `x_name` where `x` is a number, and `name` is a name for your personal reference. This will ensure that migrations are run in the correct order. Here is an example of some migration files: ::

  001_initial.py
  002_add_admin_to_users.py
  003_add_account_table.py

The basic template for a migration is as follows: ::

    def up:
      pass

    def down:
      pass

A more complete example of a migration file can be found `here <https://github.com/cam-stitt/arnold/blob/master/tests/migrations/001_initial.py>`_.
