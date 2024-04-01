import sys

from loguru import logger

import argparse
from platform import system

import utils.operations as ops


# Глобальные таски
# ToDo Добавить функции, которые отвечают за установку и удаление программы
# ToDo Логирование добавить везде, где нужно
# ToDo Переименовать некоторые объекты, чтобы было понятней, operations, uip, arguments какая-то фигня имхо


def main():
    parser = argparse.ArgumentParser(description="Simple package installer for windows")
    parser.add_argument("-lf", "--logfile", help="logfile name", dest="logfile", default='')
    parser.add_argument("-dl", "--debug-level", help="logging level", dest="debug_level",
                        choices=['debug', 'info', 'warning', 'error', 'critical'], default='info')
    operations_parser = parser.add_subparsers(title="Operations", dest="operation")

    operations = (ops.InstallOperation(),)

    for operation in operations:
        name, *aliases = operation.names

        option = operations_parser.add_parser(name,  # ToDo добавить адаптивность
                                              aliases=aliases,
                                              help=operation.help
                                              )

        for argument in operation.arguments:  # ToDo добавить адаптивность
            option.add_argument(*argument.names,
                                help=argument.help,
                                type=argument.type
                                )

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
    main()
