import sys
import argparse
import logging



class BaseCommand:
    def configure(self, parser):
        pass

    def exec(self, args):
        raise RuntimeError("Unimplemented.")


class EditCommand(BaseCommand):
    def exec(self, args):
        print("Edit")


class AddCommand(BaseCommand):
    def exec(self, args):
        print("Add")


class UpdateCommand(BaseCommand):
    def exec(self, args):
        print("Update")


class RemoveCommand(BaseCommand):
    def exec(self, args):
        print("Remove")


class ShowCommand(BaseCommand):
    def exec(self, args):
        print("Show")


class EnableCommand(BaseCommand):
    def exec(self, args):
        print("Enable")


class DisableCommand(BaseCommand):
    def exec(self, args):
        print("Disable")


class Application:
    LOGGER_FORMAT = "%(levelname)s: %(message)s"

    def __init__(self):
        self.handlers = {}
        pass

    def add_command(self, name, handler):
        if name in self.handlers:
            raise RuntimeError('Command "%s" already registered.' % name)
        self.handlers[name] = handler

    def run(self, argv):
        args = self._parse_args(argv)

        if args.verbose:
            logging.basicConfig(format=Application.LOGGER_FORMAT, level=logging.DEBUG)
        else:
            logging.basicConfig(format=Application.LOGGER_FORMAT, level=logging.INFO)

        if args.cmd not in self.handlers:
            raise RuntimeError('Unknow command "%s"' % args.cmd)
        self.handlers[args.cmd].exec(args)

    def _parse_args(self, argv):
        parser = argparse.ArgumentParser()
        parser.description = "/etc/hosts file editor"
        parser.add_argument("-v", "--verbose", action="store_true")
        # parser.add_argument("-d", "--dry-run", action="store_true")

        # Register subcommands
        subparsers = parser.add_subparsers(dest="cmd")
        for name, handler in self.handlers.items():
            handler.configure(subparsers.add_parser(name))

        return parser.parse_args(argv[1:])


if __name__ == "__main__":
    app = Application()
    app.add_command('edit', EditCommand())
    app.add_command('add', AddCommand())
    app.add_command('update', UpdateCommand())
    app.add_command('remove', RemoveCommand())
    app.add_command('show', ShowCommand())
    app.add_command('enable', EnableCommand())
    app.add_command('disable', DisableCommand())
    app.run(sys.argv)
