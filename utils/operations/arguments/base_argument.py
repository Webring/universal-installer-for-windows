from typing import Any
from argparse import ArgumentTypeError


class BaseArgument:
    def __init__(self):
        self.names = []
        self.help = "It's an empty argument"

    def type(self, value: str) -> Any:
        return value
