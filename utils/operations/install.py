import os.path

from loguru import logger

from .base_operation import BaseOperation
from .arguments.package_name_argument import PackageNameArgument
from ..functions.install_package import install_package
from ..uip.parser import parse_script_file


class InstallOperation(BaseOperation):
    def __init__(self):
        super().__init__()
        self.names = ["install"]
        self.arguments = (PackageNameArgument(),)
        self.help = "Install package on your computer"

    def execute(self, arguments: dict) -> None:
        logger.info("Start installing package on your computer")
        package_path = arguments["package"]
        logger.info(f"Opening file '{package_path}'")

        data = parse_script_file(package_path)
        data["path_to_package"] = os.path.abspath(package_path)
        install_package(data)
