# WARNING! Deprecated

I do not have the capacity to maintain this project. Please feel free to fork the repo and apply your updates there, however I will not be updating this repo any further.

[![Build Status](https://travis-ci.org/cam-stitt/arnold.png)](https://travis-ci.org/cam-stitt/arnold)

#arnold - Migrations for peewee

arnold is a python package to assist in managing migrations for the [peewee](https://github.com/coleifer/peewee) orm.

A full example application can be viewed at [cam-stitt/arnold-example](https://github.com/cam-stitt/arnold-example).

##Installation

Installation is simple using pip:

`pip install arnold`

##Usage

###The arnold_config folder
To generate the arnold config folder, run the following command:

```
arnold init
```

This will create a directory and fill it with the default content. The directory will look like this:

```
.
+-- arnold_config
|   +-- __init__.py
|   +-- migrations
|       +-- __init__.py
```

You can provide an option for a custom folder name by using the `--folder` option. Note that if you provide a custom folder, you will have to pass the `--folder` option to all future arnold commands.

###Creating Migrations

Migrations are easy to setup. Simply create a `migration` folder
(with an `__init__.py`) and then start creating your migrations.

Migrations require two methods. `up` for creation and `down` for deletion.

Peewee has the ability to easily perform migrations such as adding a column. See [peewee docs](http://peewee.readthedocs.org/en/latest/peewee/playhouse.html#basic-schema-migrations).

You must follow the naming convention `x_name` where `x` is a number, and `name` is a name for your personal reference. This will ensure that migrations are run in the correct order. Here is an example of some migration files:

```
001_initial.py
002_add_admin_to_users.py
003_add_account_table.py
```

An example of a migration file can be found [here](https://github.com/cam-stitt/arnold/blob/master/tests/migrations/001_initial.py).

###Running Migrations

Migrations are run in a stepwise manner. There are two commands available to run migrations in a particular direction. Both of these commands require a number to tell arnold how many migrations you would like to run.

```
arnold up 1
```

The above command will run 1 migration upwards, if available.

```
arnold down 3
```

The above command will run 3 migrations downwards.

If you pass in a count of `0`, arnold will run all migrations that have not yet been run.

```
arnold up 0
```

The first time that this is run, the [Migration](https://github.com/cam-stitt/arnold/blob/master/arnold/models.py) table will be added.

###Status

You can also request the status of the database by running `arnold status`. It will print the latest migration name and the date that it was completed.

###Configuration

Arnold accepts a number of configuration options to the commands.

* --folder - The folder to use for configration/migrations.
* --fake   - Add the row to the database without running the migration.

The `__init__.py` file inside the configuration folder holds the database value. This should be peewee database value. Here is an example `__init__.py` file:

```python
from peewee import SqliteDatabase

database = SqliteDatabase('test.db')
```

##Contribute

Ideas or Pull Requests to make this project better are always welcome.

- Issue Tracker: https://github.com/cam-stitt/arnold/issues
- Source Code: https://github.com/cam-stitt/arnold

##Support

If you are having issues, please let us know.

##License

The project is licensed under the BSD license.

##Roadmap

At this point, I don't have any items on the roadmap. If you have any ideas, please create an issue.
