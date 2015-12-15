import os
import sys

import argparse

from termcolor import colored

from arnold.exceptions import DirectionNotFoundException
from arnold.models import Migration
from importlib import import_module


class Terminator:
    IGNORED_FILES = ["__init__"]

    def __init__(self, args):
        self.fake = getattr(args, 'fake', False)
        self.count = getattr(args, 'count', 0)
        self.folder = getattr(args, 'folder', None)

        self.prepare_config()
        self.database = self.config.database
        self.prepare_model()

    def prepare_config(self):
        self.config = import_module(self.folder)

    def prepare_model(self):
        self.model = Migration
        self.model._meta.database = self.database

        self._setup_table()

    def _setup_table(self):
        if self.model.table_exists():
            return False
        else:
            self.model.create_table()
        return True

    def _retreive_filenames(self):
        files = os.listdir('{0}/{1}'.format(self.folder, 'migrations'))
        filenames = list()
        for f in files:
            splits = f.rsplit(".", 1)
            if len(splits) <= 1 or splits[1] != "py" or \
               splits[0] in self.IGNORED_FILES:
                continue
            filenames.append(splits[0])
        return sorted(filenames, key=lambda fname: int(fname.split("_")[0]))

    def _perform_single_migration(self, migration):
        """Runs a single migration method (up or down)"""
        migration_exists = self.model.select().where(
            self.model.migration == migration
        ).limit(1).exists()

        if migration_exists and self.direction == "up":
            print("Migration {0} already exists, {1}".format(
                colored(migration, "yellow"), colored("skipping", "cyan")
            ))
            return False
        if not migration_exists and self.direction == "down":
            print("Migration {0} does not exist, {1}".format(
                colored(migration, "yellow"), colored("skipping", "cyan")
            ))
            return False

        print("Migration {0} going {1}".format(
            colored(migration, "yellow"), colored(self.direction, "magenta")
        ))

        if self.fake:
            self._update_migration_table(migration)
            print(
                "Faking {0}".format(colored(migration, "yellow"))
            )
        else:
            module_name = "{0}.{1}.{2}".format(
                self.folder, 'migrations', migration
            )
            print("Importing {0}".format(
                colored(module_name, "blue")
            ))
            migration_module = import_module(module_name)

            if hasattr(migration_module, self.direction):
                getattr(migration_module, self.direction)()
                self._update_migration_table(migration)
            else:
                raise DirectionNotFoundException

        print("Migration {0} went {1}".format(
            colored(migration, "yellow"), colored(self.direction, "magenta")
        ))
        return True

    def _update_migration_table(self, migration):
        if self.direction == "up":
            self.model.insert(migration=migration).execute()
        else:
            self.model.delete().where(
                self.model.migration == migration
            ).execute()

    def get_latest_migration(self):
        return self.model.select().order_by(
            self.model.migration.desc()
        ).first()

    def perform_migrations(self, direction):
        """
        Find the migration if it is passed in and call the up or down method as
        required. If no migration is passed, loop through list and find
        the migrations that need to be run.
        """
        self.direction = direction

        filenames = self._retreive_filenames()

        if self.direction == "down":
            filenames.reverse()

        if len(filenames) <= 0:
            return True

        start = 0

        latest_migration = self.get_latest_migration()

        if latest_migration:
            migration_index = filenames.index(latest_migration.migration)

            if migration_index == len(filenames) - 1 and \
                self.direction == 'up':
                print("Nothing to go {0}.".format(
                    colored(self.direction, "magenta"))
                )
                return False

            if self.direction == 'up':
                start = migration_index + 1
            else:
                start = migration_index
        if not latest_migration and self.direction == 'down':
            print("Nothing to go {0}.".format(
                colored(self.direction, "magenta"))
            )
            return False

        if self.count == 0:
            end = len(filenames)
        else:
            end = start + self.count

        migrations_to_complete = filenames[start:end]

        if self.count > len(migrations_to_complete):
            print(
                "Count {0} greater than available migrations. Going {1} {2} times."
                .format(
                    colored(self.count, "green"),
                    colored(self.direction, "magenta"),
                    colored(len(migrations_to_complete), "red"),
                )
            )

        for migration in migrations_to_complete:
            self._perform_single_migration(migration)
        return True


def up(args):
    Terminator(args).perform_migrations('up')


def down(args):
    Terminator(args).perform_migrations('down')


def status(args):
    latest_migration = Terminator(args).get_latest_migration()
    if latest_migration:
        print("Migration {0} run at {1}.".format(
            colored(latest_migration.migration, "blue"),
            colored(latest_migration.applied_on, "green"),
        ))
    else:
        print("No migrations currently run.")


def init(args):
    os.makedirs('{0}/migrations'.format(args.folder))
    open('{0}/__init__.py'.format(args.folder), 'a').close()
    open('{0}/migrations/__init__.py'.format(args.folder), 'a').close()
    return True


def parse_args(args):
    sys.path.insert(0, os.getcwd())
    parser = argparse.ArgumentParser(description='Migrations. Down. Up.')
    subparsers = parser.add_subparsers(help='sub-command help')

    init_cmd = subparsers.add_parser('init', help='Create the config folder.')
    init_cmd.set_defaults(func=init)

    if args[0] == 'init':
        init_cmd.add_argument(
            '--folder', default='arnold_config', help='The folder to create.'
        )
    else:
        parser.add_argument(
            '--folder', dest='folder', default='arnold_config',
            help='The folder that contains arnold files.'
        )

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

    return parser.parse_args(args)

def main():
    sys.argv.pop(0)
    args = parse_args(sys.argv)
    args.func(args)
