Running Migrations
------------------

To begin running migrations, add a file at the root of your project and give it a name such as `migrator.py`. Copy and paste the following into the file: ::

  import argparse
  from arnold import main

  parser = argparse.ArgumentParser(description="Perform migrations on the database")
  parser.add_argument("direction", help="The direction of the migrations")
  parser.add_argument("--fake", action="store_true", default=False, help="Do you want to fake the migrations (not actually run them, but update the migration table)?")

  args = parser.parse_args()

  main(
      direction=args.direction
      database=SqliteDatabase('test.db'),
      directory="path/to/migrations",
      migration_module="path.to.migrations",
      fake=args.fake
  )

Then, you can just run this from the command line: ::

  $ python migrator.py "up"

If you don't like typing python, make the file executable by running the following. ::

  chmod +x migrator.py

The first time that this is run, the `Migration <https://github.com/cam-stitt/arnold/blob/master/arnold/models.py>`_ table will be added.
