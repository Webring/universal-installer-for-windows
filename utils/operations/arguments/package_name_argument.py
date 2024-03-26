import os

from .base_argument import *


class PackageNameArgument(BaseArgument):
    def __init__(self):
        self.names = ["package"]
        self.help = "Path to package file (.uiw file)"

    def type(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise ArgumentTypeError(f"File \"{file_path}\" does not exist")
        return file_path
