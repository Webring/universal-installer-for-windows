import os.path

from loguru import logger

from .base_operation import BaseOperation
from .arguments.agree_argument import AgreeArgument
from .arguments.package_name_argument import PackageNameArgument
from ..functions.install_package import install_package
from ..uip.parser import parse_script_file


class InstallOperation(BaseOperation):
    def __init__(self):
        super().__init__()
        self.names = ["install"]
        self.arguments = (PackageNameArgument(), AgreeArgument())
        self.help = "Install package on your computer"

    def execute(self, arguments: dict) -> None:
        package_path = arguments["package"]
        logger.info(f"Opening file '{package_path}'")
        data = parse_script_file(package_path)

        if not data["parse_success"]:
            return

        if arguments["agree"] is None:
            answer = input(f"Do you want to install '{data['title']}'? [Yes/no] ").lower()
            arguments["agree"] = (answer in ("", "yes", "y"))

        if not arguments["agree"]:
            logger.info(f"You refused to install '{data["title"]}' application")
            return

        logger.info("Start installing package on your computer")
        data["path_to_package"] = os.path.abspath(package_path)
        installation_success = install_package(data)

        if installation_success:
            logger.success(f"Package '{data['title']}' successfully installed on your computer")
        else:
            logger.critical(f"Failed to install '{data['title']}' application")