import argparse, configparser

parser = argparse.ArgumentParser()

parser.add_argument("operation",
                    help="",  # ToDo write a help message
                    choices=["install",
                             "remove",
                             "info"]
                    )

parser.add_argument("package",
                    help=""  # ToDo write a help message
                    )

args = parser.parse_args()
