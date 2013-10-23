import os

from termcolor import colored

from shift.exceptions import (
    ArgumentException,
    DBAttrNotFound,
    DirectionNotFoundException,
    InvalidConfiguration,
    ModuleNotFoundException,
    MigrationNotFoundException,
)
from shift.models import Migration
from shift.utils import import_module


IGNORED_FILES = [u"__init__"]


def _retreive_filenames(files):
    filenames = list()
    for f in files:
        splits = f.rsplit(u".", 1)
        if len(splits) <= 1 or splits[1] != u"py" or \
           splits[0] in IGNORED_FILES:
            continue
        filenames.append(splits[0])
    return filenames


def _perform_single_migration(settings, direction, migration, model):
    """Runs a single migration method (up or down)"""
    if model.select().where(
        model.migration == migration
    ).exists() and direction == "up":
        print(u"Migration {0} already exists, {1}".format(
            colored(migration, u"yellow"), colored(u"skipping", u"cyan")
        ))
        return False
    print(u"Migration {0} going {1}".format(
        colored(migration, u"yellow"), colored(direction, u"magenta")
    ))
    try:
        migration_module = import_module(u"{0}.{1}".format(
            getattr(settings, "MIGRATION_MODULE"), migration)
        )
    except:
        raise ModuleNotFoundException

    if hasattr(migration_module, direction):
        getattr(migration_module, direction)()
        if direction == u"up":
            model.insert(migration=migration).execute()
            print(u"Migration {0} went {1}".format(
                migration, colored(u"up", u"magenta")
            ))
        else:
            model.delete().where(
                model.migration == migration
            ).execute()
            print(u"Migration {0} went {1}".format(
                migration, colored(u"down", u"magenta")
            ))
        return True
    else:
        raise DirectionNotFoundException


def _perform_migrations(settings, direction, model, migration=None):
    """
    Find the migration if it is passed in and call the up or down method as
    required. If no migration is passed, loop through list and find
    the migrations that need to be run.
    """
    files = os.listdir(getattr(settings, "MIGRATION_DIR"))
    filenames = _retreive_filenames(files)
    if migration:
        if migration not in filenames:
            raise MigrationNotFoundException
        _perform_single_migration(settings, direction, migration, model)
        return True

    for f in filenames:
        _perform_single_migration(settings, direction, f, model)
    return True


if __name__ == u"__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description=u"Simple, extendable migrations"
    )
    parser.add_argument(
        u"--direction",
        required=False,
        default=u"up",
        help=u"The direction the migration is going"
    )
    parser.add_argument(
        u"--migration",
        required=False,
        help=u"The specific migration to run"
    )
    parser.add_argument(
        u"--settings",
        required=True,
        help=u"The location of the settings file"
    )

    args = parser.parse_args()

    if args.direction not in [u"up", u"down"]:
        raise ArgumentException

    settings = import_module(args.settings)

    if hasattr(settings, "IGNORED_FILES"):
        IGNORED_FILES.extend(getattr(settings, "IGNORED_FILES"))

    if hasattr(settings, "DATABASE"):
        model = Migration
        model._meta.database = getattr(settings, "DATABASE")
    else:
        raise DBAttrNotFound

    if not hasattr(settings, "MIGRATION_DIR") or not hasattr(
            settings, "MIGRATION_MODULE"
    ):
        raise InvalidConfiguration

    _perform_migrations(
        settings, args.direction, model, migration=args.migration
    )
