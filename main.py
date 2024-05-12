import ctypes
import sys

from loguru import logger

import argparse
from platform import system

import utils.operations as ops


def main():
    parser = argparse.ArgumentParser(description="Simple package installer for windows")
    parser.add_argument("-lf", "--logfile", help="logfile name", dest="logfile", default='')
    parser.add_argument("-ll", "--loglevel", help="logging level", dest="debug_level",
                        choices=['debug', 'info', 'warning', 'error', 'critical'], default='info')
    operations_parser = parser.add_subparsers(title="Operations", dest="operation")

    operations = (ops.InstallOperation(), ops.RemoveOperation(),)

    for operation in operations:
        name, *aliases = operation.names

        option = operations_parser.add_parser(name,  # ToDo добавить адаптивность
                                              aliases=aliases,
                                              help=operation.help
                                              )

        for argument in operation.arguments:
            argument_kwargs = argument.__dict__
            argument_names = argument_kwargs.pop("names")
            option.add_argument(*argument_names, **argument_kwargs)

        option.set_defaults(func=operation.execute)

    args = parser.parse_args()

    logger.remove()
    logger.add(sys.stderr,
               level=args.debug_level.upper(),
               format="{level} | {message}",
               colorize=True
               )

    if args.logfile:
        logger.add(args.logfile,
                   format="{time} {level} {message}",
                   rotation="1 MB",
                   level=args.debug_level.upper()
                   )

    if hasattr(args, 'func'):
        args.func(vars(args))


if __name__ == '__main__':
    if system() != 'Windows':
        raise OSError("This operating system is not Windows. This program work only on Windows.")

    if not ctypes.windll.shell32.IsUserAnAdmin():
        exit("You are not administrator.")

    main()
