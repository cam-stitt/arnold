import os

from termcolor import colored

from arnold.exceptions import (
    ArgumentException,
    DBAttrNotFound,
    DirectionNotFoundException,
    InvalidConfiguration,
    ModuleNotFoundException,
    MigrationNotFoundException,
)
from arnold.models import Migration
from importlib import import_module


IGNORED_FILES = [u"__init__"]


def _setup_table(model):
    if model.table_exists():
        return
    else:
        model.create_table()
    return True


def _retreive_filenames(files):
    filenames = list()
    for f in files:
        splits = f.rsplit(u".", 1)
        if len(splits) <= 1 or splits[1] != u"py" or \
           splits[0] in IGNORED_FILES:
            continue
        filenames.append(splits[0])
    return sorted(filenames, key=lambda fname: int(fname.split("_")[0]))


def _perform_single_migration(direction, model, **kwargs):
    """Runs a single migration method (up or down)"""
    migration = kwargs.get("migration")
    if not migration:
        raise MigrationNotFoundException

    migration_exists = model.select().where(
        model.migration == migration
    ).limit(1).exists()

    if migration_exists and direction == "up":
        print(u"Migration {0} already exists, {1}".format(
            colored(migration, u"yellow"), colored(u"skipping", u"cyan")
        ))
        return False
    if not migration_exists and direction == "down":
        print(u"Migration {0} does not exist, {1}".format(
            colored(migration, u"yellow"), colored(u"skipping", u"cyan")
        ))
        return False

    print(u"Migration {0} going {1}".format(
        colored(migration, u"yellow"), colored(direction, u"magenta")
    ))

    try:
        module_name = u"{0}.{1}".format(
            kwargs.get("migration_module"), migration
        )
        print("Importing {0}".format(
            colored(module_name, "blue")
        ))
        migration_module = import_module(module_name)
    except:
        raise ModuleNotFoundException

    if hasattr(migration_module, direction):
        getattr(migration_module, direction)()
        if direction == u"up":
            model.insert(migration=migration).execute()
        else:
            model.delete().where(
                model.migration == migration
            ).execute()
        print(u"Migration {0} went {1}".format(
            colored(migration, "yellow"), colored(direction, u"magenta")
        ))
        return True
    else:
        raise DirectionNotFoundException


def _perform_migrations(direction, model, **kwargs):
    """
    Find the migration if it is passed in and call the up or down method as
    required. If no migration is passed, loop through list and find
    the migrations that need to be run.
    """
    migration = kwargs.get("migration")
    files = os.listdir(kwargs.get("directory"))
    filenames = _retreive_filenames(files)

    if direction == "down":
        filenames.reverse()

    if len(filenames) <= 0:
        return True

    if migration:
        if migration not in filenames:
            raise MigrationNotFoundException
        _perform_single_migration(direction, model, **kwargs)
        return True

    for f in filenames:
        _perform_single_migration(direction, model, migration=f, **kwargs)
    return True


def main(direction="up", **kwargs):
    """The main method, handle exceptions and start migrations"""
    # Pop ignored and db, they aren't required later
    try:
        ignored = kwargs.pop("ignored")
    except KeyError:
        ignored = None
    try:
        db = kwargs.pop("database")
    except KeyError:
        raise DBAttrNotFound
    # Get directory and module, we need them later
    directory = kwargs.get("directory")
    migration_module = kwargs.get("migration_module")

    if direction not in [u"up", u"down"]:
        raise ArgumentException

    if ignored:
        IGNORED_FILES.extend(ignored)

    if db:
        model = Migration
        model._meta.database = db
    else:
        raise DBAttrNotFound

    _setup_table(model)

    if not directory or not migration_module:
        raise InvalidConfiguration

    _perform_migrations(
        direction, model, **kwargs
    )

    return True
