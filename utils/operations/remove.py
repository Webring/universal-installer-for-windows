import os.path

from loguru import logger

from .arguments.force_argument import ForceArgument
from .base_operation import BaseOperation
from .arguments.agree_argument import AgreeArgument
from .arguments.package_name_argument import PackageNameArgument
from ..functions.remove_package import remove_package
from ..uip.parser import parse_script_file


class RemoveOperation(BaseOperation):
    def __init__(self):
        super().__init__()
        self.names = ["remove"]
        self.arguments = (PackageNameArgument(), AgreeArgument(), ForceArgument())
        self.help = "remove package from your computer"

    def execute(self, arguments: dict) -> None:
        package_path = arguments["package"]
        logger.info(f"Opening file '{package_path}'")
        data = parse_script_file(package_path)

        if not data["parse_success"]:
            return

        if arguments["agree"] is None:
            answer = input(f"Do you want to remove '{data['title']}'? [Yes/no] ").lower()
            arguments["agree"] = (answer in ("", "yes", "y"))

        if not arguments["agree"]:
            logger.info(f"You refused to remove '{data["title"]}' application")
            return

        if arguments["force"] is None:
            print("""You need to choose the way of removing package.
            There are two of them: force and soft. 
            Soft is the way of removing files created ONLY at the step of installation.
            Force is the way of removing ALL files in this directoru.
            *Be careful when choosing a removing way, as you may remove the unintended files*""")
            answer = input(f"How do you want to remove '{data['title']}'? [Force/Soft] ").lower()
            arguments["force"] = (answer in ("force", "f"))
            if answer not in ("force","soft","f","s"):
                arguments["force"] = None


        if arguments["force"]:
            logger.info("Start removing package from your computer via force way")

        data["path_to_package"] = os.path.abspath(package_path)
        remove_package(data, arguments["force"])