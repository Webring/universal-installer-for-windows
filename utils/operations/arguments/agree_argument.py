import os

from .base_argument import *


class AgreeArgument(BaseArgument):
    def __init__(self):
        self.names = ["-y", "--yes"]
        self.help = "Consent to installation"
        self.action = 'store_const'
        self.const = True
        self.dest = "agree"

    def type(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise ArgumentTypeError(f"File \"{file_path}\" does not exist")
        return file_path
