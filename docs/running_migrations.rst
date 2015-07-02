Running Migrations
------------------

Migrations are run in a stepwise manner. There are two commands available to run migrations in a particular direction. Both of these commands require a number to tell arnold how many migrations you would like to run. ::

  arnold up 1

The above command will run 1 migration upwards, if available. ::
  
  arnold down 3

The above command will run 3 migrations downwards.

If you pass in a count of `0`, arnold will run all migrations that have not yet been run. ::

  arnold up 0

The first time that this is run, the `Migration <https://github.com/cam-stitt/arnold/blob/master/arnold/models.py>`_ table will be added.

Status
^^^^^^

You can also request the status of the database by running `arnold status`. It will print the latest migration name and the date that it was completed.
