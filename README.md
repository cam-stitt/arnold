[![Build Status](https://travis-ci.org/cam-stitt/arnold.png)](https://travis-ci.org/cam-stitt/arnold)

#arnold - Migrations for peewee

arnold is a python package to assist in managing migrations for the [peewee](https://github.com/coleifer/peewee) orm.

A full example application can be viewed at [cam-stitt/arnold-example](https://github.com/cam-stitt/arnold-example).

##Installation

Installation is simple using pip:

`pip install arnold`

##Usage

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

To begin running migrations, add a file at the root of your project and give it a name such as `migrator.py`. Copy and paste the following into the file:

```python
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
```

Then, you can just run this from the command line:

```$ python migrator.py "up"```

The first time that this is run, the [Migration](https://github.com/cam-stitt/arnold/blob/master/arnold/models.py) table will be added.

###Configuration

Arnold accepts a number of configuration options.

* *direction* - "up" or "down" - direction to migrate
* *ignored* - list of filenames to ignore (not including extension)
* *database* - the peewee database to connect to
* *directory* - the directory of the migration files eg. path/to/migrations
* *migration_module* - the module of the migrations eg. path.to.migrations

##Contribute

Ideas or Pull Requests to make this project better are always welcome.

- Issue Tracker: https://github.com/cam-stitt/arnold/issues
- Source Code: https://github.com/cam-stitt/arnold

##Support

If you are having issues, please let us know.

##License

The project is licensed under the BSD license.

##Roadmap

* Migration model configuration
