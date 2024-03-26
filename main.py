import argparse

import utils.operations as ops


def main():
    parser = argparse.ArgumentParser(description="Simple package installer for windows")
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
    if hasattr(args, 'func'):
        args.func(vars(args))


if __name__ == '__main__':
    main()
