#shift - Migrations for python

shift is a python package to assist in managing migrations for your 
orm. The list of currently supported ORMs is:

* [peewee](https://github.com/coleifer/peewee)

To use it, just create a file in your project and add the following:

```python
import shift.main

if __name__ == '__main__':
    shift.main(
        database=SqliteDatabase('test.db'),
        directory="path/to/migrations",
        migration_module="path.to.migrations"
    )
```

##Features

* Migration management for peewee
* Simple API, get started in seconds

##Installation

TODO

##Contribute

- Issue Tracker: https://github.com/cam-stitt/shift/issues
- Source Code: https://github.com/cam-stitt/shift

##Support

If you are having issues, please let us know.

##License

The project is licensed under the BSD license.
