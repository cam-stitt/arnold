import os
import sys

import argparse

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


IGNORED_FILES = ["__init__"]


def _setup_table(model):
    if model.table_exists():
        return
    else:
        model.create_table()
    return True


def _retreive_filenames(files):
    filenames = list()
    for f in files:
        splits = f.rsplit(".", 1)
        if len(splits) <= 1 or splits[1] != "py" or \
           splits[0] in IGNORED_FILES:
            continue
        filenames.append(splits[0])
    return sorted(filenames, key=lambda fname: int(fname.split("_")[0]))


def _perform_single_migration(direction, model, config, migration, args):
    """Runs a single migration method (up or down)"""
    fake = getattr(args, 'fake', False)

    migration_exists = model.select().where(
        model.migration == migration
    ).limit(1).exists()

    if migration_exists and direction == "up":
        print("Migration {0} already exists, {1}".format(
            colored(migration, "yellow"), colored("skipping", "cyan")
        ))
        return False
    if not migration_exists and direction == "down":
        print("Migration {0} does not exist, {1}".format(
            colored(migration, "yellow"), colored("skipping", "cyan")
        ))
        return False

    print("Migration {0} going {1}".format(
        colored(migration, "yellow"), colored(direction, "magenta")
    ))

    if fake:
        _update_migration_table(direction, model, migration)
        print(
            "Faking {0}".format(colored(migration, "yellow"))
        )
    else:
        module_name = "{0}.{1}.{2}".format(
            args.folder, 'migrations', migration
        )
        print("Importing {0}".format(
            colored(module_name, "blue")
        ))
        try:
            migration_module = import_module(module_name)
        except ImportError:
            raise ModuleNotFoundException(
                "Migration {0} failed to import.", module_name
            )

        if hasattr(migration_module, direction):
            getattr(migration_module, direction)()
            _update_migration_table(direction, model, migration)
        else:
            raise DirectionNotFoundException

    print("Migration {0} went {1}".format(
        colored(migration, "yellow"), colored(direction, "magenta")
    ))
    return True


def _update_migration_table(direction, model, migration):
    if direction == "up":
        model.insert(migration=migration).execute()
    else:
        model.delete().where(
            model.migration == migration
        ).execute()


def get_latest_migration(model):
    return model.select().order_by(model.migration.desc()).first()


def _perform_migrations(direction, model, config, args):
    """
    Find the migration if it is passed in and call the up or down method as
    required. If no migration is passed, loop through list and find
    the migrations that need to be run.
    """
    files = os.listdir('{0}/{1}'.format(args.folder, 'migrations'))
    filenames = _retreive_filenames(files)

    if direction == "down":
        filenames.reverse()

    if len(filenames) <= 0:
        return True

    start = 0

    latest_migration = get_latest_migration(model)

    if latest_migration:
        migration_index = filenames.index(latest_migration.migration)

        if migration_index == len(filenames) - 1 and direction == 'up':
            print("Nothing to go {0}.".format(colored(direction, "magenta")))
            return True

        if direction == 'up':
            start = migration_index + 1
        else:
            start = migration_index
    if not latest_migration and direction == 'down':
        print("Nothing to go {0}.".format(colored(direction, "magenta")))
        return True

    end = start + args.count
    migrations_to_complete = filenames[start:end]

    if args.count > len(migrations_to_complete):
        print(
            "Count {0} greater than available migrations. Going {1} {2} times."
            .format(
                colored(args.count, "green"),
                colored(direction, "magenta"),
                colored(len(migrations_to_complete), "red"),
            )
        )

    for migration in migrations_to_complete:
        _perform_single_migration(
            direction, model, config, migration, args
        )
    return True


def prepare_model(database):
    model = Migration
    model._meta.database = database

    _setup_table(model)

    return model


def prepare_config(module):
    try:
        return import_module(module)
    except ImportError:
        raise ModuleNotFoundException("Config module could not be found.")


def prepare_cmd(args):
    config = prepare_config(args.folder)
    model = prepare_model(config.database)
    return config, model


def up(args):
    config, model = prepare_cmd(args)
    _perform_migrations('up', model, config, args)


def down(args):
    config, model = prepare_cmd(args)
    _perform_migrations('down', model, config, args)


def status(args):
    config, model = prepare_cmd(args)
    latest_migration = get_latest_migration(model)
    if latest_migration:
        print("Migration {0} run at {1}.".format(
            colored(latest_migration.migration, "blue"),
            colored(latest_migration.applied_on, "green"),
        ))
    else:
        print("No migrations currently run.")


def main():
    sys.path.insert(0, os.getcwd())
    parser = argparse.ArgumentParser(description='Migrations. Down. Up.')
    parser.add_argument(
        '--folder', dest='folder', default='arnold_config',
        help='The folder that contains arnold files.'
    )
    subparsers = parser.add_subparsers(help='sub-command help')

    status_cmd = subparsers.add_parser(
        'status', help='Current migration status.'
    )
    status_cmd.set_defaults(func=status)

    up_cmd = subparsers.add_parser('up', help='Migrate up.')
    up_cmd.set_defaults(func=up)
    up_cmd.add_argument(
        'count', type=int, help='How many migrations to go up.'
    )
    up_cmd.add_argument(
        '--fake', type=bool, default=False, help='Fake the migration.'
    )

    down_cmd = subparsers.add_parser('down', help='Migrate down.')
    down_cmd.set_defaults(func=down)
    down_cmd.add_argument(
        'count', type=int, help='How many migrations to go down.'
    )

    args = parser.parse_args()
    args.func(args)
