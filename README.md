#arnold - Migrations for python

arnold is a python package to assist in managing migrations for your orm.

The list of currently supported ORMs is:

* [peewee](https://github.com/coleifer/peewee)

##Installation

Installation is simple using pip:

`pip install arnold`

##Usage

###Creating Migrations

Migrations are easy to setup. Simply create a `migration` folder
(with an `__init__.py`) and then start creating your migrations.

Migrations require two methods. `up` for creation and `down` for deletion.

Peewee has the ability to easily perform migrations such as adding a column. See [peewee docs](http://peewee.readthedocs.org/en/latest/peewee/playhouse.html#basic-schema-migrations).

You should follow a naming convention such as prefixing the file with numbers and incrementing them for each migration. This ensures that the files are run in the correct order.

An example of a migration file can be found [here](https://github.com/cam-stitt/arnold/blob/master/tests/migrations/001_initial.py).

###Running Migrations

There are a number of ways this can be done, however the following is the recommended way. Create a `bin` directory in your project and add a file called `arnold`. In this file add the following:

```python
#!/usr/bin/env python

from arnold import main
main(
    database=SqliteDatabase('test.db'),
    directory="path/to/migrations",
    migration_module="path.to.migrations"
)
```

Then, you can just run this from the command line:

`$ bin/arnold`

The first time that this is run, the [Migration](https://github.com/cam-stitt/arnold/blob/master/arnold/models.py) table will be added.

###Configuration

Arnold accepts a number of configuration options.

* *direction* - "up" or "down" - direction to migrate
* *ignored* - list of filenames to ignore (not including extension)
* *database* - the peewee database to connect to
* *directory* - the directory of the migration files eg. path/to/migrations
* *migration_module* - the module of the migrations eg. path.to.migrations

##Contribute

- Issue Tracker: https://github.com/cam-stitt/arnold/issues
- Source Code: https://github.com/cam-stitt/arnold

##Support

If you are having issues, please let us know.

##License

The project is licensed under the BSD license.

##Roadmap

* Support for more SQLAlchemy
