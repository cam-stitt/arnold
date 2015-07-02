Configuration
-------------

Arnold accepts a number of configuration options to the commands.

* --folder - The folder to use for configration/migrations.
* --fake   - Add the row to the database without running the migration.

The `__init__.py` file inside the configuration folder holds the database value. This should be peewee database value. Here is an example `__init__.py` file: ::

  from peewee import SqliteDatabase

  database = SqliteDatabase('test.db')
